# Router for the voting form page.

import psycopg
from fastapi import APIRouter, Body, Depends, HTTPException, Query, status

from src.database import db_dependency
from src.models import (
    Project,
    ProjectVote,
    Settings,
    VoteProjectInput,
    get_active_poll,
    get_projects,
    get_settings,
    get_voter,
    get_voter_votes,
    save_voter_votes,
)
from src.schemas import DataResponseSchema, ProjectSchema, VoteRequestBodySchema
from src.security import verify_valid_email, verify_valid_token

from src.logger import get_logger

logger = get_logger()

router = APIRouter()


def _create_data_response_schema(
    settings: Settings, projects: list[Project], voter_votes: list[ProjectVote], note: str
) -> DataResponseSchema:
    projects_data: dict[int, ProjectSchema] = {}
    for project in projects:
        projects_data[project.project_id] = ProjectSchema(
            id=project.project_id,
            name=project.name,
            description_1=project.description_1,
            description_2=project.description_2,
            fixed=project.fixed,
            min_points=project.min_points,
            max_points=project.max_points,
            rank=project.order_number,
            points=0,
            points_text="0",
            marked=False,
        )

    for vote in voter_votes:
        projects_data[vote.project_id].points = vote.points
        projects_data[vote.project_id].points_text = str(vote.points)
        projects_data[vote.project_id].marked = vote.points > 0

    projects_order = sorted(projects_data.values(), key=lambda x: x.rank)

    max_total_points = settings.max_total_points
    max_total_points -= sum([project.min_points for project in projects if project.fixed])

    return DataResponseSchema(
        voted=len(voter_votes) > 0,
        max_total_points=max_total_points,
        points_step=settings.points_step,
        open_for_voting=settings.open_for_voting,
        note=note,
        results=settings.results,
        projects=projects_order,
    )


@router.post("/data")
def route_data(
    email: str = Query(description="voter email"),
    token: str = Query(description="voter email as token using RSA"),
    db: psycopg.Connection = Depends(db_dependency),
) -> DataResponseSchema:
    """Get the data for the voting form page"""

    if not verify_valid_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    if not verify_valid_token(email, token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized, the token is invalid")

    settings = get_settings(db)
    projects = get_projects(db)
    votes = get_voter_votes(db, email)

    voter = get_voter(db, email)
    note = voter.note if voter is not None else ""

    return _create_data_response_schema(settings, projects, votes, note)


@router.post("/vote")
def route_vote(
    email: str = Query(description="voter email"),
    token: str = Query(description="voter email as token using RSA"),
    body: VoteRequestBodySchema = Body(description="the vote data"),
    db: psycopg.Connection = Depends(db_dependency),
) -> DataResponseSchema:
    """Save vote of voter"""
    try:
        logger.info(f"Received vote request - email: {email}")
        logger.info(f"Vote data: {body}")

        poll = get_active_poll(db)

        if not verify_valid_email(email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

        if not verify_valid_token(email, token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized, the token is invalid")

        settings = get_settings(db)

        if not settings.open_for_voting:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Voting is not open for the public")

        projects = get_projects(db)

        max_total_points = settings.max_total_points
        max_total_points -= sum([project.min_points for project in projects if project.fixed])

        projects_dict = {project.project_id: project for project in projects}

        logger.info(f"Validating vote with settings: points_step={settings.points_step}, max_total_points={settings.max_total_points}")

        # validate vote
        projects_votes = {vote.id: vote for vote in body.projects}

        if set(projects_votes.keys()) != set(projects_dict.keys()):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid project ids")

        for vote_project in projects_votes.values():
            # Check for negative values
            if vote_project.points < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Negative points are not allowed"
                )
            
            # Check points are divisible by points_step
            if vote_project.points % settings.points_step != 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Points must be divisible by {settings.points_step}"
                )
            
            project = projects_dict.get(vote_project.id)
            if project is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid project id")

            if vote_project.points > 0:
                # Check if the points are in the project range
                if vote_project.points < project.min_points or vote_project.points > project.max_points:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid points")

        total_points = sum(vote.points for vote in projects_votes.values())
        if total_points > max_total_points:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total points exceed the limit")

        ranks = {vote.rank for vote in projects_votes.values()}
        if ranks != set(range(1, len(ranks) + 1)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ranks")

        # save votes
        vote_input = [
            VoteProjectInput(
                poll_id=poll.poll_id,
                project_id=vote.id,
                points=vote.points,
                rank=vote.rank,
            )
            for vote in body.projects
        ]
        save_voter_votes(db, email, body.note, vote_input)

        # get the updated votes
        votes = get_voter_votes(db, email)

        return _create_data_response_schema(settings, projects, votes, body.note)
    
    except HTTPException as e:
        logger.error(f"Vote validation failed: {e.detail}")
        raise
