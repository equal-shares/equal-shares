# This module is the public interface (Facade) of the algorithm.

from dataclasses import dataclass

from src.algorithm.computation import min_max_equal_shares


@dataclass
class VouterItem:
    vouter_id: int
    voutes: dict[int, int]


@dataclass
class ProjectItem:
    project_id: int
    min_cost: int
    max_cost: int


@dataclass
class AlgorithmInput:
    projects: list[ProjectItem]
    voutes: list[VouterItem]
    budget: int


@dataclass
class AlgorithmResult:
    pass


def run_algorithm(data: AlgorithmInput) -> AlgorithmResult:
    bids: dict[int, dict[int, int]] = {project.project_id: dict() for project in data.projects}

    for vouter in data.voutes:
        for project_id, cost in vouter.voutes.items():
            bids[project_id][vouter.vouter_id] = cost

    min_max_equal_shares(
        voters=[vouter.vouter_id for vouter in data.voutes],
        cost_min_max=[{project.project_id: (project.min_cost, project.max_cost)} for project in data.projects],
        bids=bids,
        budget=data.budget,
    )

    return AlgorithmResult()
