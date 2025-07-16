import logging

from src.algorithm.equal_shares import equal_shares
from src.algorithm.utils import (
    calculate_average_bids,
    check_allocations,
    get_project_min_costs,
    plot_bid_data,
    remove_zero_bids,
)

logger = logging.getLogger("min_max_equal_shares_logger")


def min_max_equal_shares(
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
            bids (dict): A dictionary mapping project IDs to the list of voters
                         who approve them and the cost the voters chose.
            budget (int): The total budget available
            use_plt (bool): if it is True, the function will use matplotlib

    >>> import numpy as np
    >>> voters = [1, 2]
    >>> cost_min_max=[{11: (200, 300)}, {12: (300,400)}, {13: (100,150)}]
    >>> bids = {11: {1: 500, 2: 200}, 12: {1: 300, 2: 300}, 13: {2: 100}}
    >>> winners_allocations, candidates_payments_per_voter = min_max_equal_shares(
    ...     voters, cost_min_max, 900, bids, use_plt=False
    ... )
    >>> {k: int(np.round(v)) for k, v in winners_allocations.items()}
    {11: 500, 12: 300, 13: 100}
    """
    projects_min_costs = get_project_min_costs(cost_min_max)
    bids_not_zero = remove_zero_bids(bids)
    winners_allocations, candidates_payments_per_voter = equal_shares(voters, projects_min_costs, budget, bids_not_zero)

    averages = calculate_average_bids(bids_not_zero, voters)
    logger.debug("averages: %s", averages)

    if not check_allocations(cost_min_max, winners_allocations):
        raise ValueError("the budget allocation is not valid")

    if use_plt:
        plot_bid_data(bids_not_zero, cost_min_max, averages, winners_allocations)

    rounded_winners_allocations = {
        project_id: int(allocation) for project_id, allocation in winners_allocations.items()
    }

    return rounded_winners_allocations, candidates_payments_per_voter
