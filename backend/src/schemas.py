# contains the API schemas
# schema - object that the API return or receive

from pydantic import BaseModel


class ProjectSchema(BaseModel):
    """Project with the data of voter."""

    id: int
    name: str
    description_1: str
    description_2: str
    fixed: bool
    min_points: int
    max_points: int
    rank: int
    points: int
    points_text: str
    marked: bool


class VotedProjectSchema(BaseModel):
    id: int
    rank: int
    points: int
    marked: bool


class DataResponseSchema(BaseModel):
    voted: bool
    max_total_points: int
    points_step: int
    open_for_voting: bool
    projects: list[ProjectSchema]


class VoteRequestBodySchema(BaseModel):
    projects: list[VotedProjectSchema]
