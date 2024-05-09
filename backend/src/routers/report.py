# Router for the reports and the algorithm.

from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from src.config import config

router = APIRouter()


@router.get("/data")
def route_report_data(admin_key: UUID = Query(description="key for authentication of admin")) -> dict:
    if config.admin_key != admin_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return {"data": "report data"}
