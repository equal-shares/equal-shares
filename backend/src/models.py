# Handle all the database models and queries
# model - a class that represents a table in the database
# query - or "named query" is a function that performs a query on the database

from datetime import datetime

import psycopg
from fastapi import HTTPException, status
from psycopg.types.json import Json
from pydantic import BaseModel, field_serializer

from src.database import db_named_query

# Deprecated tables, if table removed it should be here!
_DEPRECATED_TABLES_NAMES: list[str] = []

# All tables that used in the project should be here!
_TABLES_NAMES = ["polls", "settings", "projects", "voters", "projects_votes"]


@db_named_query
def get_tables_exists(db: psycopg.Connection) -> dict[str, bool]:
    """Check if the tables exist in the database."""
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
            """,
        )

        rows = cursor.fetchall()

    tables_exists = {table_name: False for table_name in _TABLES_NAMES}

    for row in rows:
        if row[0] in tables_exists:
            tables_exists[row[0]] = True

    return tables_exists


@db_named_query
def delete_tables(db: psycopg.Connection) -> None:
    """Delete the tables in the database."""
    with db.cursor() as cursor:
        for table_name in _DEPRECATED_TABLES_NAMES + _TABLES_NAMES:
            cursor.execute(f"DROP TABLE IF EXISTS public.{table_name};")
        db.commit()


@db_named_query
def create_tables(db: psycopg.Connection) -> None:
    """Create the tables in the database."""
    with db.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE public.polls (
                poll_id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                active BOOLEAN NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.settings (
                poll_id INTEGER NOT NULL,
                max_total_points INTEGER NOT NULL,
                points_step INTEGER NOT NULL,
                open_for_voting BOOLEAN NOT NULL,
                results JSON
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.projects (
                poll_id INTEGER NOT NULL,
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                min_points INTEGER NOT NULL,
                max_points INTEGER NOT NULL,
                description_1 TEXT NOT NULL,
                description_2 TEXT NOT NULL,
                fixed BOOLEAN NOT NULL,
                order_number INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL,
                UNIQUE(poll_id, name)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.voters (
                poll_id INTEGER NOT NULL,
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                note VARCHAR(1024) NOT NULL,
                created_at TIMESTAMP NOT NULL,
                UNIQUE(poll_id, email)
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.projects_votes (
                poll_id INTEGER NOT NULL,
                voter_id INTEGER NOT NULL,
                project_id INTEGER NOT NULL,
                points INTEGER NOT NULL,
                rank INTEGER NOT NULL,
                UNIQUE(voter_id, project_id),
                UNIQUE(voter_id, rank)
            );
            """
        )
        db.commit()


class Poll(BaseModel):
    """A poll is a collection of projects, users and votes. Only one poll can be active at a time."""

    poll_id: int
    name: str
    active: bool


@db_named_query
def create_poll(db: psycopg.Connection, name: str) -> Poll:
    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO public.polls (name, active)
            VALUES (%s, FALSE)
            RETURNING poll_id;
            """,
            (name,),
        )
        db.commit()

        row = cursor.fetchone()
        assert row is not None

        poll_id = int(row[0])

        cursor.execute(
            """
            INSERT INTO public.settings (poll_id, max_total_points, points_step, open_for_voting)
            VALUES (%s, 1000, 100, FALSE);
            """,
            (poll_id,),
        )
        db.commit()

    return Poll(poll_id=poll_id, name=name, active=False)


@db_named_query
def get_poll_by_name(db: psycopg.Connection, name: str) -> Poll | None:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT poll_id, name, active
            FROM public.polls
            WHERE name = %s;
            """,
            (name,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return Poll(poll_id=row[0], name=row[1], active=row[2])


@db_named_query
def get_poll_by_id(db: psycopg.Connection, poll_id: int) -> Poll | None:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT poll_id, name, active
            FROM public.polls
            WHERE poll_id = %s;
            """,
            (poll_id,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return Poll(poll_id=row[0], name=row[1], active=row[2])


@db_named_query
def get_polls(db: psycopg.Connection) -> list[Poll]:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT poll_id, name, active
            FROM public.polls;
            """,
        )
        rows = cursor.fetchall()

    return [Poll(poll_id=row[0], name=row[1], active=row[2]) for row in rows]


@db_named_query
def set_poll_active(db: psycopg.Connection, poll_id: int) -> None:
    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.polls
            SET active = FALSE;
            """,
        )
        cursor.execute(
            """
            UPDATE public.polls
            SET active = TRUE
            WHERE poll_id = %s;
            """,
            (poll_id,),
        )
        db.commit()


@db_named_query
def get_active_poll(db: psycopg.Connection) -> Poll:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT poll_id, name, active
            FROM public.polls
            WHERE active = TRUE;
            """,
        )
        row = cursor.fetchone()

    if row is None:
        # This should never happen
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No active poll found")

    return Poll(poll_id=row[0], name=row[1], active=row[2])


class Settings(BaseModel):
    """Settings for the application that can be changed by the admin."""

    poll_id: int
    max_total_points: int
    points_step: int
    open_for_voting: bool
    results: dict | None


@db_named_query
def update_settings(db: psycopg.Connection, settings: Settings) -> None:
    poll_id = get_active_poll(db).poll_id

    results = Json(settings.results) if settings.results is not None else None

    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.settings
            SET max_total_points = %s, points_step = %s, open_for_voting = %s, results = %s
            WHERE poll_id = %s;
            """,
            (settings.max_total_points, settings.points_step, settings.open_for_voting, results, poll_id),
        )

        db.commit()


@db_named_query
def get_settings(db: psycopg.Connection) -> Settings:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            (
                """
            SELECT max_total_points, points_step, open_for_voting, results
            FROM public.settings
            WHERE poll_id = %s;
            """
            ),
            (poll_id,),
        )
        row = cursor.fetchone()

        assert row is not None

    return Settings(
        poll_id=poll_id,
        max_total_points=row[0],
        points_step=row[1],
        open_for_voting=row[2],
        results=row[3],
    )


@db_named_query
def delete_projects_and_votes(db: psycopg.Connection) -> None:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.projects WHERE poll_id = %s;", (poll_id,))
        cursor.execute("DELETE FROM public.projects_votes WHERE poll_id = %s;", (poll_id,))
        cursor.execute("DELETE FROM public.voters WHERE poll_id = %s;", (poll_id,))
        db.commit()


@db_named_query
def delete_votes(db: psycopg.Connection) -> None:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.projects_votes WHERE poll_id = %s;", (poll_id,))
        cursor.execute("DELETE FROM public.voters WHERE poll_id = %s;", (poll_id,))
        db.commit()


class Project(BaseModel):
    """A project that can be voted on."""

    poll_id: int
    project_id: int = 0
    name: str
    min_points: int
    max_points: int
    description_1: str
    description_2: str
    fixed: bool
    order_number: int
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.isoformat()


@db_named_query
def create_project(
    db: psycopg.Connection,
    name: str,
    min_points: int,
    max_points: int,
    description_1: str,
    description_2: str,
    fixed: bool,
    order_number: int,
) -> Project:
    poll_id = get_active_poll(db).poll_id

    project = Project(
        poll_id=poll_id,
        name=name,
        min_points=min_points,
        max_points=max_points,
        description_1=description_1,
        description_2=description_2,
        fixed=fixed,
        order_number=order_number,
        created_at=datetime.now(),
    )

    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO public.projects
            (poll_id, name, min_points, max_points, description_1, description_2, fixed, order_number, created_at)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                project.poll_id,
                project.name,
                project.min_points,
                project.max_points,
                project.description_1,
                project.description_2,
                project.fixed,
                project.order_number,
                project.created_at,
            ),
        )
        db.commit()

        row = cursor.fetchone()
        assert row is not None

        project.project_id = int(row[0])

    return project


@db_named_query
def check_project_exists(db: psycopg.Connection, name: str) -> bool:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM public.projects
            WHERE poll_id = %s AND name = %s;
            """,
            (poll_id, name),
        )
        row = cursor.fetchone()

    return row is not None


@db_named_query
def get_projects(db: psycopg.Connection) -> list[Project]:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, min_points, max_points, description_1, description_2, fixed, order_number, created_at
            FROM public.projects
            WHERE poll_id = %s
            ORDER BY order_number, created_at;
            """,
            (poll_id,),
        )
        rows = cursor.fetchall()

    return [
        Project(
            poll_id=poll_id,
            project_id=row[0],
            name=row[1],
            min_points=row[2],
            max_points=row[3],
            description_1=row[4],
            description_2=row[5],
            fixed=bool(row[6]),
            order_number=row[7],
            created_at=row[8],
        )
        for row in rows
    ]


class Voter(BaseModel):
    """A voter that can vote on projects."""

    poll_id: int
    voter_id: int = 0
    email: str
    note: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.isoformat()


class ProjectVote(BaseModel):
    """A vote for a project from a voter."""

    poll_id: int
    voter_id: int
    project_id: int
    points: int
    rank: int


class VoteProjectInput(BaseModel):
    poll_id: int
    project_id: int
    points: int
    rank: int


class VoteData(BaseModel):
    """Single voter's votes."""

    poll_id: int
    voter: Voter
    projects: list[ProjectVote]


@db_named_query
def get_voter(db: psycopg.Connection, email: str) -> Voter | None:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, note, created_at
            FROM public.voters
            WHERE poll_id = %s AND email = %s;
            """,
            (poll_id, email),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return Voter(poll_id=poll_id, voter_id=row[0], email=row[1], note=row[2], created_at=row[3])


@db_named_query
def save_voter_votes(db: psycopg.Connection, email: str, note: str, projects: list[VoteProjectInput]) -> Voter:
    """
    Save the votes of a voter.
    If the voter does not exist, it will be created.
    Will delete all previous votes of the voter.
    """

    poll_id = get_active_poll(db).poll_id

    voter = Voter(poll_id=poll_id, email=email, note=note, created_at=datetime.now())

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT poll_id, email FROM public.voters WHERE poll_id = %s AND email = %s;
            """,
            (poll_id, voter.email),
        )
        voter_exists = cursor.fetchone() is not None

    if not voter_exists:
        with db.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.voters (poll_id, email, note, created_at)
                VALUES (%s, %s, %s, %s);
                """,
                (poll_id, voter.email, voter.note, voter.created_at),
            )
            db.commit()

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id FROM public.voters WHERE poll_id = %s AND email = %s;
            """,
            (poll_id, email),
        )
        db.commit()
        row = cursor.fetchone()
        assert row is not None

        voter.voter_id = int(row[0])

    with db.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM public.projects_votes WHERE poll_id = %s AND voter_id = %s;
            """,
            (poll_id, voter.voter_id),
        )
        db.commit()

    with db.cursor() as cursor:
        for project in projects:
            cursor.execute(
                """
                INSERT INTO public.projects_votes (poll_id, voter_id, project_id, points, rank)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (poll_id, voter.voter_id, project.project_id, project.points, project.rank),
            )

        db.commit()

    return voter


@db_named_query
def get_votes(db: psycopg.Connection) -> list[VoteData]:
    """get all votes from the database."""

    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT v.id, v.email, v.note, v.created_at, pv.project_id, pv.points, pv.rank
            FROM public.voters AS v
            JOIN public.projects_votes AS pv ON pv.voter_id = v.id
            WHERE v.poll_id = %s
            ORDER BY v.created_at, pv.rank;
            """,
            (poll_id,),
        )
        rows = cursor.fetchall()

    votes: dict[int, VoteData] = {}
    for row in rows:
        voter_id = row[0]
        if voter_id not in votes:
            votes[voter_id] = VoteData(
                poll_id=poll_id,
                voter=Voter(poll_id=poll_id, voter_id=voter_id, email=row[1], note=row[2], created_at=row[3]),
                projects=[],
            )

        votes[voter_id].projects.append(
            ProjectVote(
                poll_id=poll_id,
                voter_id=voter_id,
                project_id=row[4],
                points=row[5],
                rank=row[6],
            )
        )

    return list(votes.values())


@db_named_query
def get_voter_votes(db: psycopg.Connection, email: str) -> list[ProjectVote]:
    poll_id = get_active_poll(db).poll_id

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT v.id, pv.project_id, pv.points, pv.rank
            FROM public.voters AS v
            JOIN public.projects_votes AS pv ON v.id = pv.voter_id
            WHERE v.poll_id = %s AND v.email = %s
            ORDER BY pv.project_id;
            """,
            (poll_id, email),
        )
        rows = cursor.fetchall()

    votes: list[ProjectVote] = []
    for row in rows:
        votes.append(ProjectVote(poll_id=poll_id, voter_id=row[0], project_id=row[1], points=row[2], rank=row[3]))

    return votes
