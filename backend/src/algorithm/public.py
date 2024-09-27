# This module is the public interface (Facade) of the algorithm.

from dataclasses import dataclass

from src.logger import get_logger

logger = get_logger()


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
    raw_result: tuple[dict[int, int], dict[int, dict[int, float]]]


def run_algorithm(data: AlgorithmInput) -> AlgorithmResult:
    for vouter in data.voutes:
        sum_bid = 0
        for project_id, cost in vouter.voutes.items():
            sum_bid += cost
        if sum_bid > data.budget:
            logger.info(f"ERROR: vouter_id={vouter.vouter_id}, sum_bid={sum_bid}")
        else:
            logger.info(f"OK: vouter_id={vouter.vouter_id}, sum_bid={sum_bid}")

    bids: dict[int, dict[int, int]] = {
        _get_project_algorithm_id(data.projects, project.project_id): dict() for project in data.projects
    }

    for vouter in data.voutes:
        for project_id, cost in vouter.voutes.items():
            bids[_get_project_algorithm_id(data.projects, project_id)][
                _get_voter_algorithm_id(data.voutes, vouter)
            ] = cost

    voters = [_get_voter_algorithm_id(data.voutes, vouter) for vouter in data.voutes]
    cost_min_max = [
        {_get_project_algorithm_id(data.projects, project.project_id): (project.min_cost, project.max_cost)}
        for project in data.projects
    ]

    # logger.info(f"voters: {voters}")
    # logger.info(f"cost_min_max: {cost_min_max}")
    # logger.info(f"bids: {bids}")
    # logger.info(f"budget: {data.budget}")

    winners_allocations: dict = {}
    candidates_payments_per_voter: dict = {}

    logger.info(f"voters: {voters}")
    logger.info(f"cost_min_max: {cost_min_max}")
    logger.info(f"bids: {bids}")
    logger.info(f"budget: {data.budget}")

    # winners_allocations, candidates_payments_per_voter = min_max_equal_shares(
    #     voters=voters,
    #     cost_min_max=cost_min_max,
    #     bids=bids,
    #     budget=data.budget,
    # )

    logger.info(f"winners_allocations: {winners_allocations}")
    logger.info(f"candidates_payments_per_voter: {candidates_payments_per_voter}")

    return AlgorithmResult(raw_result=(winners_allocations, candidates_payments_per_voter))


def _get_voter_algorithm_id(voutes: list[VouterItem], vouter: VouterItem) -> int:
    for i, vouter_item in enumerate(voutes):
        if vouter_item.vouter_id == vouter.vouter_id:
            return i + 1

    raise ValueError(f"Vouter {vouter.vouter_id} not found")


def _get_project_algorithm_id(projects: list[ProjectItem], project_id: int) -> int:
    for i, project_item in enumerate(projects):
        if project_item.project_id == project_id:
            return i + 1

    raise ValueError(f"Project {project_id} not found")
