# Router for management endpoints by admin

import urllib.parse
from io import BytesIO
from uuid import UUID

import pandas as pd
import psycopg
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status

from src.config import config
from src.database import db_dependency
from src.models import (
    Settings,
    check_project_exists,
    create_project,
    create_tables,
    delete_projects_and_votes,
    delete_votes,
    get_projects,
    get_settings,
    get_tables_exists,
    update_settings,
)
from src.security import create_token, verify_valid_email, verify_valid_token

router = APIRouter()


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


@router.get("/delete-projects-and-votes")
def route_delete_projects_and_votes(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Delete all projects and votes from the database"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    delete_projects_and_votes(db)

    return {"status": "ok", "message": "All projects and votes have been deleted"}


@router.get("/delete-votes")
def route_delete_votes(
    admin_key: UUID = Query(description="key for authentication of admin"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Delete all votes from the database"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    delete_votes(db)

    return {"status": "ok", "message": "All votes have been deleted"}


@router.post("/set-settings")
async def route_set_settings(
    admin_key: UUID = Query(description="key for authentication of admin"),
    max_total_points: int = Query(description="the maximum total points a voter can give to all the projects in total"),
    points_step: int = Query(description="the step of points that can be given to a project"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """Update the custom settings for the application"""

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    if max_total_points < points_step or points_step < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid settings")

    update_settings(db, Settings(max_total_points=max_total_points, points_step=points_step))

    return {
        "max_total_points": max_total_points,
        "points_step": points_step,
    }


@router.post("/add-projects")
async def route_add_projects(
    admin_key: UUID = Query(description="key for authentication of admin"),
    xlsx_file: UploadFile = File(description="XLSX file with the projects data"),
    db: psycopg.Connection = Depends(db_dependency),
) -> dict:
    """
    Add projects to the database from a XLSX file. \\
    The XLSX file must have the following columns:
    - Project name
    - Min points
    - Max points
    - unused column - can be anything
    - Description
    """

    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    content = await xlsx_file.read()
    file = BytesIO(content)

    df = pd.read_excel(file)

    # Validate the File
    if len(df.columns) < 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing columns")

    projects_data: list[dict] = []

    for i in range(len(df)):
        row = list(df.iloc[i])
        project_name, min_points, max_points, _, description = list(row)

        if not project_name or not min_points or not max_points or not description:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Row {i + 1}: Missing data")

        project_name = str(project_name).strip()
        min_points = str(min_points).split(".", 2)[0].strip()
        max_points = str(max_points).split(".", 2)[0].strip()
        description = str(description).strip()

        if not min_points.isdigit() or not max_points.isdigit():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Row {i + 1}: Points must be numbers")

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
                "description": description,
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
        "settings": {
            "max_total_points": settings.max_total_points,
            "points_step": settings.points_step,
        },
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
