# Router for the reports and the algorithm.

from enum import StrEnum
import io
import json
import sys
import traceback
import zipfile
from datetime import datetime
from uuid import UUID

import pandas as pd
import psycopg
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, Response, status

from pydantic import BaseModel
from src.algorithm.public import AlgorithmInput, AlgorithmResult, ProjectItem, VouterItem, run_algorithm
from src.config import config
from src.database import db_dependency, get_db
from src.logger import get_logger
from src.models import Project, Settings, VoteData, get_projects, get_settings, get_votes


logger = get_logger()

router = APIRouter()


class InMemoryZip:
    def __init__(self) -> None:
        self.zip_buffer = io.BytesIO()

    def add_file(self, file_name: str, file_contents: str | bytes) -> None:
        with zipfile.ZipFile(self.zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr(file_name, file_contents)

    def get_content(self) -> bytes:
        self.zip_buffer.seek(0)
        content = self.zip_buffer.getvalue()
        self.zip_buffer.close()
        return content


class ReportStatus(StrEnum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


class Report:
    status: ReportStatus
    text_files: dict[str, str]
    binary_files: dict[str, bytes]
    _last_exeption_id: int

    def __init__(self) -> None:
        self.status = ReportStatus.CREATED
        self.text_files = {}
        self.binary_files = {}
        self._last_exeption_id = 0

    def generate_exeption_id(self) -> int:
        self._last_exeption_id += 1
        return self._last_exeption_id

    def append_text_to_file(self, file_name: str, file_contents: str) -> None:
        if file_name in self.text_files:
            self.text_files[file_name] += file_contents
        else:
            self.text_files[file_name] = file_contents

    def add_binary_file(self, file_name: str, file_contents: bytes) -> None:
        self.binary_files[file_name] = file_contents

    def get_content(self) -> bytes:
        zip_file = InMemoryZip()
        for file_name, text in self.text_files.items():
            zip_file.add_file(file_name, text)

        for file_name, content in self.binary_files.items():
            zip_file.add_file(file_name, content)

        return zip_file.get_content()


class ReportsStorage:
    def __init__(self) -> None:
        self.reports: dict[int, Report] = {}

    def create_report(self) -> int:
        if len(self.reports) == 0:
            report_id = 1
        else:
            report_id = max(self.reports.keys()) + 1

        self.reports[report_id] = Report()
        return report_id

    def get_report(self, report_id: int) -> Report:
        return self.reports[report_id]

    def remove_report(self, report_id: int) -> None:
        self.reports.pop(report_id)


reports_storage = ReportsStorage()


class ReportStarted(BaseModel):
    report_id: int


@router.get("/start")
def start_report_route(
    background_tasks: BackgroundTasks,
    admin_key: UUID = Query(description="key for authentication of admin"),
) -> ReportStarted:
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    report_id = reports_storage.create_report()

    background_tasks.add_task(create_report_task, report_id)

    return ReportStarted(report_id=report_id)


class ReportStatusResponse(BaseModel):
    report_id: int
    status: ReportStatus
    is_finished: bool


@router.get("/status")
def status_report_route(
    admin_key: UUID = Query(description="key for authentication of admin"),
    report_id: int = Query(description="id of the report"),
) -> ReportStatusResponse:
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    report = reports_storage.get_report(report_id)
    return ReportStatusResponse(
        report_id=report_id,
        status=report.status,
        is_finished=report.status == ReportStatus.FINISHED,
    )


@router.get("/result")
def get_report_route(
    admin_key: UUID = Query(description="key for authentication of admin"),
    report_id: int = Query(description="id of the report"),
    remove_report: bool = Query(description="if the report should be removed after downloading", default=True),
) -> Response:
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    report = reports_storage.get_report(report_id)

    if remove_report:
        if report.status != ReportStatus.FINISHED:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not finished")

        content = report.get_content()

        reports_storage.remove_report(report_id)
    else:
        content = report.get_content()

    return Response(
        content=content,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=report.zip"},
    )


def create_report_task(report_id: int) -> None:
    with get_db() as db:
        report = reports_storage.get_report(report_id)
        report.status = ReportStatus.IN_PROGRESS
        try:
            _create_report(report, db)
        except Exception:
            _report_log_error(report, "Error while creating report")
        report.status = ReportStatus.FINISHED


def _create_report(report: Report, db: psycopg.Connection) -> None:
    _report_log_info(report, "Starting report creation")

    _report_log_info(report, "Getting the data from the database")

    try:
        settings, projects, votes = _report_load_data(report, db)
        _report_log_info(report, "Data from the database retrieved")
    except Exception:
        return

    if len(projects) == 0:
        _report_log_error(report, "No projects found", without_exeption=True)
        return

    if len(votes) == 0:
        _report_log_error(report, "No votes found", without_exeption=True)
        return

    _report_log_info(report, "Save the data as csv files")
    try:
        _report_save_data_as_csv(report, projects, votes)
        _report_log_info(report, "Data saved as csv files")
    except Exception:
        _report_log_error(report, "Error while saving data as csv files")

    _report_log_info(report, "Run the algorithm")
    try:
        result = _report_run_algorithm(report, settings, projects, votes)
        _report_log_info(report, "Algorithm finished")
    except Exception:
        _report_log_error(report, "Error while running the algorithm")

    _report_log_info(report, "Report creation finished")

    _report_log_info(report, "Save the result in readable format")
    try:
        _report_save_result_as_csv(report, result)
        _report_log_info(report, "Result saved as csv files")
    except Exception:
        _report_log_error(report, "Error while saving result as csv files")


def _report_log_info(report: Report, log: str) -> None:
    _report_log(report, "INFO", log)


def _report_log_error(report: Report, log: str, without_exeption: bool = False) -> None:
    _report_log(report, "ERROR", log)

    if not without_exeption:
        ex = sys.exc_info()[1]
        if ex is not None:
            log = str(ex) + "\n\n" + traceback.format_exc()
            expected_id = report.generate_exeption_id()

            _report_log(report, "ERROR", log, only_in_full=True)
            report.append_text_to_file(f"error_{expected_id}.txt", log)


def _report_log(report: Report, level: str, log: str, only_in_full: bool = False) -> None:
    if level == "INFO":
        logger.info(log)
    elif level == "ERROR":
        logger.error(log)

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not only_in_full:
        report.append_text_to_file("log.txt", f"{created_at} {level}: {log}\n")
    report.append_text_to_file("full-log.txt", f"{created_at} {level}: {log}\n")


def _report_load_data(report: Report, db: psycopg.Connection) -> tuple[Settings, dict[int, Project], list[VoteData]]:
    settings = None
    projects_records = None
    votes = None

    try:
        settings = get_settings(db)
        report.append_text_to_file("db_settings.json", json.dumps(settings.model_dump(), indent=4))
    except Exception:
        _report_log_error(report, "Error while getting data from the database")

    try:
        projects_records = get_projects(db)
        report.append_text_to_file(
            "db_projects.json", json.dumps([project.model_dump() for project in projects_records], indent=4)
        )
    except Exception:
        _report_log_error(report, "Error while getting data from the database")

    try:
        votes = get_votes(db)
        report.append_text_to_file("db_votes.json", json.dumps([vote.model_dump() for vote in votes], indent=4))
    except Exception:
        _report_log_error(report, "Error while getting data from the database")

    if settings is None or projects_records is None or votes is None:
        raise Exception

    projects = {project.project_id: project for project in projects_records}

    return settings, projects, votes


def _report_save_data_as_csv(report: Report, projects: dict[int, Project], votes: list[VoteData]) -> None:
    raw_projects_df = pd.DataFrame([project.model_dump() for project in projects.values()])

    flat_voutes = []
    for vote in votes:
        for item in vote.projects:
            project = projects[item.project_id]
            flat_voutes.append(
                {
                    "voter_id": vote.voter.voter_id,
                    "email": vote.voter.email,
                    "project_id": item.project_id,
                    "project_name": project.name,
                    "rank": item.rank,
                    "points": item.points,
                }
            )

    raw_votes_df = pd.DataFrame([flat_voutes])

    report.append_text_to_file("raw_projects.csv", raw_projects_df.to_csv(index=False))
    report.append_text_to_file("raw_votes.csv", raw_votes_df.to_csv(index=False))

    projects_df = raw_projects_df.copy()
    projects_df = projects_df[["project_id", "name", "min_points", "max_points"]]

    voters_df = pd.DataFrame([vote.voter.model_dump() for vote in votes])
    votes_df = voters_df.copy()

    votes_df = votes_df[["voter_id", "email"]]
    for project in projects.values():
        votes_df[str(project.project_id) + "_rank"] = None
        votes_df[str(project.project_id) + "_points"] = None

    for vote in votes:
        for item in vote.projects:
            votes_df.loc[votes_df["voter_id"] == vote.voter.voter_id, str(item.project_id) + "_rank"] = item.rank
            votes_df.loc[votes_df["voter_id"] == vote.voter.voter_id, str(item.project_id) + "_points"] = item.points

    report.append_text_to_file("projects.csv", projects_df.to_csv(index=False))
    report.append_text_to_file("voters.csv", voters_df.to_csv(index=False))
    report.append_text_to_file("votes.csv", votes_df.to_csv(index=False))


def _report_run_algorithm(
    report: Report, settings: Settings, projects: dict[int, Project], votes: list[VoteData]
) -> AlgorithmResult:
    input_data = AlgorithmInput(
        projects=[
            ProjectItem(
                project_id=project.project_id,
                min_cost=project.min_points,
                max_cost=project.max_points,
            )
            for project in projects.values()
        ],
        voutes=[
            VouterItem(
                vouter_id=vote.voter.voter_id, voutes={project.project_id: project.points for project in vote.projects}
            )
            for vote in votes
        ],
        budget=settings.max_total_points,
    )

    _report_log_info(report, "Start computation")
    result = run_algorithm(input_data)
    _report_log_info(report, "Computation finished")

    report.append_text_to_file("raw_result.json", json.dumps(result.raw_result, indent=4))

    return result


def _report_save_result_as_csv(report: Report, result: AlgorithmResult) -> None:
    pass
