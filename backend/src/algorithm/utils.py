import logging

logger = logging.getLogger("equal_shares_logger")


def find_max(bids: dict[int, dict[int, int]]) -> dict[int, int]:
    """
    T.0
    >>> bids = {
    ...     1: {1: 100, 2: 100, 4: 100},
    ...     2: {2: 150, 5: 150},
    ...     3: {1: 200, 5: 200},
    ...     4: {3: 250, 4: 250},
    ...     5: {2: 300, 3: 300, 5: 300},
    ...     6: {2: 350, 5: 350},
    ...     7: {1: 400, 4: 400},
    ...     8: {2: 450, 5: 450},
    ...     9: {1: 500, 3: 500, 5: 500},
    ...     10: {2: 550, 3: 550}
    ... }
    >>> find_max(bids)
    {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    """
    max_cost_for_project = {}
    for project_id, voter_bids in bids.items():
        max_cost_for_project[project_id] = max(voter_bids.values())
    return max_cost_for_project


def filter_bids(
    update_bids, update_approvers, curr_project_id, curr_project_cost, budget_increment_per_project, update_cost
):

    max_payment = curr_project_cost + budget_increment_per_project
    filtered_approvers = {voter: bid for voter, bid in update_bids[curr_project_id].items() if bid <= max_payment}
    update_bids[curr_project_id] = filtered_approvers
    update_approvers[curr_project_id] = list(filtered_approvers.keys())
    update_cost[curr_project_id] = max_payment
