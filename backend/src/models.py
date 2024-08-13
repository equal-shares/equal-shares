# Handle all the database models and queries
# model - a class that represents a table in the database
# query - or "named query" is a function that performs a query on the database

from datetime import datetime

import psycopg
from pydantic import BaseModel, field_serializer

from src.database import db_named_query

_TABLES_NAMES = ["settings", "projects", "voters", "projects_votes"]


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
def create_tables(db: psycopg.Connection) -> None:
    """Create the tables in the database."""
    with db.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE public.settings (
                max_total_points INTEGER NOT NULL,
                points_step INTEGER NOT NULL
            );
            """
        )

        cursor.execute(
            """
            INSERT INTO public.settings (max_total_points, points_step)
            VALUES (1000, 1000)
            ON CONFLICT DO NOTHING;
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.projects (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                min_points INTEGER NOT NULL,
                max_points INTEGER NOT NULL,
                description_1 TEXT NOT NULL,
                description_2 TEXT NOT NULL,
                fixed BOOLEAN NOT NULL,
                order_number INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.voters (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP NOT NULL
            );
            """
        )

        cursor.execute(
            """
            CREATE TABLE public.projects_votes (
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


class Settings(BaseModel):
    """Settings for the application that can be changed by the admin."""

    max_total_points: int
    points_step: int


@db_named_query
def update_settings(db: psycopg.Connection, settings: Settings) -> None:
    with db.cursor() as cursor:
        cursor.execute(
            """
            UPDATE public.settings
            SET max_total_points = %s, points_step = %s;
            """,
            (settings.max_total_points, settings.points_step),
        )

        db.commit()


@db_named_query
def get_settings(db: psycopg.Connection) -> Settings:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT max_total_points, points_step
            FROM public.settings;
            """
        )
        row = cursor.fetchone()
        assert row is not None

    return Settings(max_total_points=row[0], points_step=row[1])


@db_named_query
def delete_projects_and_votes(db: psycopg.Connection) -> None:
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.projects;")
        cursor.execute("DELETE FROM public.projects_votes;")
        cursor.execute("DELETE FROM public.voters;")
        db.commit()


@db_named_query
def delete_votes(db: psycopg.Connection) -> None:
    with db.cursor() as cursor:
        cursor.execute("DELETE FROM public.projects_votes;")
        cursor.execute("DELETE FROM public.voters;")
        db.commit()


class Project(BaseModel):
    """A project that can be voted on."""

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
    project = Project(
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
            (name, min_points, max_points, description_1, description_2, fixed, order_number, created_at)
            VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
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
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT 1
            FROM public.projects
            WHERE name = %s;
            """,
            (name,),
        )
        row = cursor.fetchone()

    return row is not None


@db_named_query
def get_projects(db: psycopg.Connection) -> list[Project]:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, name, min_points, max_points, description_1, description_2, fixed, order_number, created_at
            FROM public.projects
            ORDER BY order_number, created_at;
            """
        )
        rows = cursor.fetchall()

    return [
        Project(
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

    voter_id: int = 0
    email: str
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        return value.isoformat()


class ProjectVote(BaseModel):
    """A vote for a project from a voter."""

    voter_id: int
    project_id: int
    points: int
    rank: int


class VoteProjectInput(BaseModel):
    project_id: int
    points: int
    rank: int


class VoteData(BaseModel):
    """Single voter's votes."""

    voter: Voter
    projects: list[ProjectVote]


@db_named_query
def get_voter(db: psycopg.Connection, email: str) -> Voter | None:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, email, created_at
            FROM public.voters
            WHERE email = %s;
            """,
            (email,),
        )
        row = cursor.fetchone()

    if row is None:
        return None

    return Voter(voter_id=row[0], email=row[1], created_at=row[2])


@db_named_query
def save_voter_votes(db: psycopg.Connection, email: str, projects: list[VoteProjectInput]) -> Voter:
    """
    Save the votes of a voter.
    If the voter does not exist, it will be created.
    Will delete all previous votes of the voter.
    """

    voter = Voter(email=email, created_at=datetime.now())

    with db.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO public.voters (email, created_at)
            VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING;
            """,
            (voter.email, voter.created_at),
        )
        db.commit()

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT id FROM public.voters WHERE email = %s;
            """,
            [email],
        )
        db.commit()
        row = cursor.fetchone()
        assert row is not None

        voter.voter_id = int(row[0])

    with db.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM public.projects_votes WHERE voter_id = %s;
            """,
            [voter.voter_id],
        )
        db.commit()

    with db.cursor() as cursor:
        for project in projects:
            cursor.execute(
                """
                INSERT INTO public.projects_votes (voter_id, project_id, points, rank)
                VALUES (%s, %s, %s, %s);
                """,
                (voter.voter_id, project.project_id, project.points, project.rank),
            )

        db.commit()

    return voter


@db_named_query
def get_votes(db: psycopg.Connection) -> list[VoteData]:
    """get all votes from the database."""

    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT v.id, v.email, v.created_at, pv.project_id, pv.points, pv.rank
            FROM public.voters AS v
            JOIN public.projects_votes AS pv ON pv.voter_id = v.id
            ORDER BY v.created_at, pv.rank;
            """
        )
        rows = cursor.fetchall()

    votes: dict[int, VoteData] = {}
    for row in rows:
        voter_id = row[0]
        if voter_id not in votes:
            votes[voter_id] = VoteData(voter=Voter(voter_id=voter_id, email=row[1], created_at=row[2]), projects=[])

        votes[voter_id].projects.append(ProjectVote(voter_id=voter_id, project_id=row[3], points=row[4], rank=row[5]))

    return list(votes.values())


@db_named_query
def get_voter_votes(db: psycopg.Connection, email: str) -> list[ProjectVote]:
    with db.cursor() as cursor:
        cursor.execute(
            """
            SELECT v.id, pv.project_id, pv.points, pv.rank
            FROM public.voters AS v
            JOIN public.projects_votes AS pv ON v.id = pv.voter_id
            WHERE v.email = %s
            ORDER BY pv.project_id;
            """,
            [email],
        )
        rows = cursor.fetchall()

    votes: list[ProjectVote] = []
    for row in rows:
        votes.append(ProjectVote(voter_id=row[0], project_id=row[1], points=row[2], rank=row[3]))

    return votes
