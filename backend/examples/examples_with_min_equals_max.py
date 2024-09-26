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





def main() -> None:
    get_logger(LoggerName.ALGORITHM).setLevel(logging.DEBUG)
    get_logger(LoggerName.ALGORITHM).addHandler(logging.StreamHandler(sys.stderr))

    # test_min_max_equal_shares_passed_3()
    example1()


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())

    main()
