"""
Examples in which the minimum of each project is equal to the maximum.
The outcome should be the same as the standard Method of Equal Shares.
"""

import logging
import sys

from src.algorithm.equal_shares import equal_shares, equal_shares_fixed_budget
from src.algorithm.equal_shares_original import equal_shares as equal_shares_original
from src.algorithm.utils import find_max
from src.logger import LoggerName, get_logger
from collections import defaultdict


def bids_from_approvals(approval_ballots: dict[int,set], projects_costs:dict[int,float]):
    """
    Given approval votes and project costs, creates bids assuming the minimum of each project equals its maximum.

    >>> bids_from_approvals( {1: {11,12,13}, 2: {11,13,15}, 3: {11,14}} , {11:110, 12:120, 13:130, 14:140, 15:150})
    {11: {1: 110, 2: 110, 3: 110}, 12: {1: 120}, 13: {1: 130, 2: 130}, 15: {2: 150}, 14: {3: 140}}
    """
    result = defaultdict(dict)
    for voter_id, approvals in approval_ballots.items():
        for project_id in approvals:
            result[project_id][voter_id] = projects_costs[project_id]
    return dict(result)



def bids_from_reverse_approvals(reverse_approval_ballots: dict[int,set], projects_costs:dict[int,float]):
    """
    Given approval votes and project costs, creates bids assuming the minimum of each project equals its maximum.

    >>> bids_from_reverse_approvals( {11: {1,2,3}, 12: {1}, 13: {1,2}, 14:{3}, 15:{2}}, {11:110, 12:120, 13:130, 14:140, 15:150})
    {11: {1: 110, 2: 110, 3: 110}, 12: {1: 120}, 13: {1: 130, 2: 130}, 14: {3: 140}, 15: {2: 150}}
    """
    result = defaultdict(dict)
    for project_id, approvals in reverse_approval_ballots.items():
        for voter_id in approvals:
            result[project_id][voter_id] = projects_costs[project_id]
    return dict(result)


def example1() -> None:
    print("Running example 1")

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 15: 300, 19: 500}
    approvals = {
        11: [1, 2, 4],
        12: [2, 5],
        13: [1, 5],
        15: [2, 3, 5],
        19: [1, 3, 5],
    }
    bids = bids_from_reverse_approvals(approvals, projects_costs)
    budget = 900

    winners_allocation, candidates_payments_per_voter = equal_shares(
        voters, projects_costs, budget, bids
    )
    print("Our MES: ", winners_allocation)
    
    winners_allocation = equal_shares_original(
        voters, projects_costs.keys(), projects_costs, approvals, budget
    )
    print("Original MES: ", winners_allocation)


def example2() -> None:
    print("Running example 2")

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {
            3: 250,
            4: 250,
        },
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {
            1: 400,
            4: 400,
        },
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500, 5: 500},
        20: {2: 550, 3: 550},
    }
    budget = 900

    winners_allocation, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    print("winners_allocation", winners_allocation)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


def example3() -> None:
    print("Running example 3")

    voters = [1, 2]
    projects_costs = {11: 200, 12: 300, 13: 100}
    bids = {11: {1: 500, 2: 200}, 12: {1: 300, 2: 300}, 13: {2: 100}}
    budget = 900
    winners_allocation, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    print("winners_allocation", winners_allocation)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


def example4() -> None:
    print("Running example 4")

    voters = [1, 2, 3]
    projects_costs = {11: 100, 12: 100}
    # No increments
    bids = {
        11: {1: 300, 2: 150},
        12: {2: 150, 3: 300},
    }
    budget = 300

    max_bid_for_project = find_max(bids)
    winners_allocation, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    print("winners_allocation", winners_allocation)
    print("updated_cost", updated_cost)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


def example5() -> None:
    print("Running example 5")

    voters = list(range(100))
    projects_costs = {11: 0, 12: 0}
    # No increments
    bids = {
        11: {i: 100 for i in range(100)},
        12: {i: 100 for i in range(99)},
    }
    budget = 100

    max_bid_for_project = find_max(bids)
    winners_allocation, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    print("winners_allocation", winners_allocation)
    print("updated_cost", updated_cost)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


def test_min_max_equal_shares_passed_3() -> None:
    """
    Two projects with the same amount of voters and the price difference between them is 1
    """

    voters = [1, 2]
    projects_costs = {11: 99, 12: 98}
    bids = {11: {2: 99}, 12: {1: 98}}
    budget = 100

    winners_allocations, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    expected_winners_allocations = {11: 0, 12: 98}
    expected_candidates_payments_per_voter = {11: {2: 0}, 12: {1: 98.0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def main() -> None:
    get_logger(LoggerName.ALGORITHM).setLevel(logging.DEBUG)
    get_logger(LoggerName.ALGORITHM).addHandler(logging.StreamHandler(sys.stderr))

    # test_min_max_equal_shares_passed_3()
    example1()


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

    main()
