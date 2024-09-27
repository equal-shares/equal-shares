# Router for management endpoints by admin

import urllib.parse
from io import BytesIO
from uuid import UUID

import pandas as pd
import psycopg
from fastapi import APIRouter, Body, Depends, File, HTTPException, Query, UploadFile, status

from src.config import config
from src.database import db_dependency
from src.models import (
    check_project_exists,
    create_poll,
    create_project,
    create_tables,
    delete_projects_and_votes,
    delete_tables,
    delete_votes,
    get_active_poll,
    get_poll_by_id,
    get_poll_by_name,
    get_polls,
    get_projects,
    get_settings,
    get_tables_exists,
    set_poll_active,
    update_settings,
)
from src.security import create_token, verify_valid_email, verify_valid_token

router = APIRouter()


@router.delete("/delete-tables")
def route_delete_tables(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    # Delete all the tables in the database
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    delete_tables(db)

    return {"status": "ok", "message": "All tables have been deleted"}


@router.get("/create-tables")
def route_create_tables(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Create all the tables in the database"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    tables_exists = get_tables_exists(db)

    if any(tables_exists.values()):
        return {
            "status": "error",
            "message": "Tables already exist",
            "tables_exists": [table_name for table_name, table_exists in tables_exists.items() if table_exists],
            "tables_not_exists": [table_name for table_name, table_exists in tables_exists.items() if not table_exists],
        }

    create_tables(db)

    return {"status": "ok", "message": "Tables have been created"}


@router.get("/polls/list")
def route_get_polls_list(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Show all the Polls"""
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    polls = get_polls(db)

    return {"polls": [poll.model_dump() for poll in polls]}


@router.get("/polls/active")
def route_get_active_poll(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Show the active Poll"""
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    poll = get_active_poll(db)

    return {"poll": poll.model_dump()}


@router.post("/polls/create")
def route_create_poll(
    admin_key: UUID = Query(description="key for authentication of admin"),
    name: str = Query(description="the name of the poll"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Create a new Poll
    Note:
    * The poll will not be active by default and closed for voting
    * For active the poll use the `/admin/polls/set-active` endpoint
    * For opening the poll for voting use the `/admin/set-settings` endpoint.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    poll = get_poll_by_name(db, name)

    if poll is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Poll already exists")

    poll = create_poll(db, name)

    return {"poll": poll.model_dump()}


@router.post("/polls/set-active")
def route_set_active_poll(
    admin_key: UUID = Query(description="key for authentication of admin"),
    poll_id: int | None = Query(
        description="the id of the poll to set as active, need only poll_id or name", default=None
    ),
    name: str | None = Query(
        description="the name of the poll to set as active, need only poll_id or name", default=None
    ),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Set the active Poll
    Note:
    * It will make the poll active but will not open for voting.
    * For opening the poll for voting use the `/admin/set-settings` endpoint.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if poll_id is None and name is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Need poll_id or name")

    if poll_id is not None and name is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Need only poll_id or name")

    if poll_id is not None:
        poll = get_poll_by_id(db, poll_id)

    if name is not None:
        poll = get_poll_by_name(db, name)

    if poll is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Poll not found")

    set_poll_active(db, poll.poll_id)

    poll = get_poll_by_id(db, poll.poll_id)

    assert poll is not None

    return {"message": "Poll has been set as active", "poll": poll.model_dump()}


@router.delete("/delete-projects-and-votes")
def route_delete_projects_and_votes(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    # Delete ALL projects and votes from the poll
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    delete_projects_and_votes(db)

    return {"status": "ok", "message": "All projects and votes have been deleted"}


@router.delete("/delete-votes")
def route_delete_votes(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    # Delete all votes from the poll
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    delete_votes(db)

    return {"status": "ok", "message": "All votes have been deleted"}


@router.post("/set-settings")
async def route_set_settings(
    admin_key: UUID = Query(description="key for authentication of admin"),
    max_total_points: int | None = Query(
        description="the maximum total points a voter can give to all the projects in total", default=None
    ),
    points_step: int | None = Query(description="the step of points that can be given to a project", default=None),
    open_for_voting: bool | None = Query(
        description="if the Poll is open for voting or not", default=None, enum=[True, False]
    ),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Update the settings for the poll.
    Note:
    * All the changes are optional
    * If open_for_voting is set to True, the poll will be open for voting and
      if False the poll will be closed for voting.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    settings = get_settings(db)

    if max_total_points is not None:
        settings.max_total_points = max_total_points

    if points_step is not None:
        settings.points_step = points_step

    if open_for_voting is not None:
        settings.open_for_voting = open_for_voting

    if settings.max_total_points < settings.points_step or settings.points_step < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid settings")

    update_settings(db, settings)

    settings = get_settings(db)

    return {
        "max_total_points": settings.max_total_points,
        "points_step": settings.points_step,
        "open_for_voting": settings.open_for_voting,
    }


@router.post("/remove-results")
def route_remove_results(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Remove the results of the poll.
    Remove the results that are showed in the form page on the graph if the poll is closed for voting.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    settings = get_settings(db)
    settings.results = None

    update_settings(db, settings)

    return {"status": "ok", "message": "Results have been removed"}


@router.post("/set-results")
def route_set_results(
    admin_key: UUID = Query(description="key for authentication of admin"),
    results: dict[int, int] = Body(description="the results of the poll", examples=[{1: 100, 2: 300, 3: 150}]),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Set the results of the poll
    Set the results that are showed in the form page on the graph if the poll is closed for voting.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    results_keys = list(results.keys())

    if len(results_keys) != len(set(results_keys)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Results cannot have duplicate project ids")

    settings = get_settings(db)
    projects = get_projects(db)

    projects_ids = {project.project_id for project in projects}

    if set(results_keys) != projects_ids:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Results must have all the projects")

    settings.results = results

    update_settings(db, settings)

    return {"status": "ok", "message": "Results have been set"}


@router.post("/add-projects")
async def route_add_projects(
    admin_key: UUID = Query(description="key for authentication of admin"),
    xlsx_file: UploadFile = File(description="XLSX file with the projects data"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Add new projects to the poll from a XLSX file. \\
    The XLSX file must have the following columns:
    - Project name
    - Min points
    - Max points
    - Description 2
    - Description 1
    - Is fixed project - if this column is 'v' then the project cannot be selected.
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    content = await xlsx_file.read()
    file = BytesIO(content)

    df = pd.read_excel(file)

    # Validate the File
    if len(df.columns) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing columns")

    projects_data: list[dict] = []

    for i in range(len(df)):
        row = list(df.iloc[i])
        project_name, min_points, max_points, description_2, description_1, fixed = list(row)

        if not project_name or not min_points or not max_points or not description_1 or not description_2:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Row {i + 1}: Missing data")

        project_name = str(project_name).strip()
        min_points = str(min_points).split(".", 2)[0].strip()
        max_points = str(max_points).split(".", 2)[0].strip()
        description_1 = str(description_1).strip()
        description_2 = str(description_2).strip()
        fixed = str(fixed).strip().lower() == "v"

        if not min_points.isdigit() or not max_points.isdigit():
            continue

        min_points = int(min_points)
        max_points = int(max_points)

        if min_points < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Row {i + 1}: Points cannot be negative"
            )

        if min_points > max_points:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Row {i + 1}: Min points cannot be greater than max points",
            )

        projects_data.append(
            {
                "name": project_name,
                "min_points": min_points,
                "max_points": max_points,
                "description_1": description_1,
                "description_2": description_2,
                "fixed": fixed,
                "order_number": len(projects_data) + 1,
            }
        )

    # Create the projects

    projects = []
    already_exists = 0

    for project_data in projects_data:
        if check_project_exists(db, project_data["name"]):
            already_exists += 1
        else:
            project = create_project(db, **project_data)
            projects.append(project)

    return {
        "status": "ok",
        "new_projects_count": len(projects),
        "already_exists": already_exists,
        "projects_count": projects,
    }


@router.get("/projects")
def route_get_projects(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Get the projects and settings"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    settings = get_settings(db)
    projects = get_projects(db)

    return {
        "settings": settings,
        "projects": projects,
    }


@router.get("/create-token")
def route_create_token(
    admin_key: UUID = Query(description="key for authentication of admin"),
    email: str = Query(description="the input email"),
) -> dict:
    """Create a token for a given email using RSA"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if not verify_valid_email(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")

    token = create_token(email)

    return {
        "email": email,
        "token": token,
        "verify": verify_valid_token(email, token),
        "quety": "?" + urllib.parse.urlencode({"email": email, "token": token}),
    }
