"""
An algorithm that runs the Average mechanism, funds all projects whose average is above their minimum,
   and then runs another algorithm (e.g. MES) on the remaining budget and projects.
"""

import copy
import logging

from src.algorithm.equal_shares import equal_shares
from src.algorithm.utils import (
    calculate_average_bids,
    check_allocations,
    get_project_min_costs,
    plot_bid_data,
    remove_zero_bids,
)

logger = logging.getLogger(__name__)


def average_first(
    voters: list[int],
    cost_min_max: list[dict[int, tuple[int, int]]],
    budget: float,
    bids: dict[int, dict[int, int]],
    use_plt: bool = True,
) -> tuple[dict[int, int], dict[int, dict[int, float]]]:
    """
    The purpose of min_max_equal_shares function is to convert the input in the received format
    to a format suitable for the equal_shares function (Selects the minimum value)
        Args:
            voters (list): A list of voter names.
            cost_min_max (dict): A dictionary mapping project IDs to their min and max costs.
            bids (dict): A dictionary mapping project IDs to the list of voters who approve
                        them and the cost the voters chose.
            budget (int): The total budget available
            use_plt (bool): if it is True, the function will use matplotlib

    >>> voters = [1, 2]
    >>> cost_min_max=[{11: (200, 500)}, {12: (300,300)}, {13: (100,150)}]
    >>> bids = {11: {1: 500, 2: 200}, 12: {1: 300, 2: 300}, 13: {2: 100}}
    >>> calculate_average_bids(bids, voters)
    {11: 350.0, 12: 300.0, 13: 50.0}
    >>> winners_allocations, candidates_payments_per_voter = average_first(
    ...     voters, cost_min_max, 900, bids, use_plt=False
    ... )
    >>> {k: np.round(v) for k, v in winners_allocations.items()}  # {11: 499.0, 12: 300, 13: 100}
    {11: 350.0, 12: 300.0, 13: 100}
    """
    projects_min_costs = get_project_min_costs(cost_min_max)
    bids_not_zero = remove_zero_bids(bids)
    averages = calculate_average_bids(bids_not_zero, voters)
    logger.debug("averages: %s", averages)

    projects_min_costs = {}
    for item in copy.deepcopy(cost_min_max):
        project_id, (min_value, _) = item.popitem()
        projects_min_costs[project_id] = min_value

    winners_allocations = {}
    for project_id, min_cost in projects_min_costs.items():
        if averages[project_id] >= min_cost:
            allocation = int(averages[project_id])
            winners_allocations[project_id] = allocation
            projects_min_costs[project_id] = 0

            # Update bids:
            bids_not_zero[project_id] = {
                voter: max(0, bid - allocation) for voter, bid in bids_not_zero[project_id].items()
            }
            budget -= allocation
        else:
            winners_allocations[project_id] = 0
            projects_min_costs[project_id] = min_cost
    winners_additional_allocations, candidates_payments_per_voter = equal_shares(
        voters, projects_min_costs, budget, bids_not_zero
    )

    for project_id, average in averages.items():
        winners_allocations[project_id] += winners_additional_allocations[project_id]

    if not check_allocations(cost_min_max, winners_allocations):
        raise ValueError("the budget allocation is not valid")

    if use_plt:
        plot_bid_data(bids_not_zero, cost_min_max, averages, winners_allocations)
    return winners_allocations, candidates_payments_per_voter
