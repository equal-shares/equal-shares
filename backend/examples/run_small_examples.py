import logging
import sys

from src.algorithm.equal_shares import equal_shares, equal_shares_fixed_budget
from src.algorithm.utils import find_max
from src.logger import LoggerName, get_logger


def example1() -> None:
    print("Running example 1")

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 15: 300, 19: 500}
    # No increments
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        15: {2: 300, 3: 300, 5: 300},
        19: {1: 500, 3: 500, 5: 500},
    }

    # With increments
    bids = {
        11: {1: 100, 2: 150, 4: 200},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 300},
        15: {2: 300, 3: 350, 5: 400},
        19: {1: 500, 3: 500, 5: 500},
    }
    budget = 900

    max_bid_for_project = find_max(bids)
    winners_allocation, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    print("winners_allocation", winners_allocation)
    print("updated_cost", updated_cost)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


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

    voters = [1, 2]
    projects_costs = {11: 100, 12: 150}
    bids = {11: {1: 100}, 12: {2: 150}}
    budget = 300
    winners_allocation, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    print("winners_allocation", winners_allocation)
    print("candidates_payments_per_voter", candidates_payments_per_voter)


def example6() -> None:
    print("Running example 6")

    voters = [1, 2, 3]
    projects_costs = {11: 100, 12: 100, 13: 100}
    bids = {11: {1: 600, 2: 700, 3: 400}, 12: {1: 400, 2: 300, 3: 600}, 13: {1: 0, 2: 0, 3: 0}}
    budget = 1000
    winners_allocation, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    print("winners_allocation", winners_allocation)
    print("candidates_payments_per_voter", candidates_payments_per_voter)
    logging.getLogger("equal_shares_logger").setLevel(logging.INFO)
    logging.getLogger("equal_shares_logger").addHandler(logging.StreamHandler(sys.stderr))

    voters = [1, 2]
    projects_costs = {11: 100, 12: 100, 13: 100}
    bids = {11: {1: 600, 2: 700}, 12: {1: 400, 2: 300}, 13: {1: 0, 2: 0}}
    budget = 1000
    # winners_allocation, candidates_payments_per_voter = equal_shares(voters, projects_costs, budget, bids,)
    equal_shares_fixed_budget(voters, projects_costs, 1479, bids, {11:700, 12:400, 13:0})


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

    # expected_winners_allocations = {11: 0, 12: 98}
    # expected_candidates_payments_per_voter = {11: {2: 0}, 12: {1: 98.0}}

    # assert winners_allocations == expected_winners_allocations

    # assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    # for key in candidates_payments_per_voter:
    #     assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def main() -> None:
    get_logger(LoggerName.ALGORITHM).setLevel(logging.DEBUG)
    get_logger(LoggerName.ALGORITHM).addHandler(logging.StreamHandler(sys.stderr))

    test_min_max_equal_shares_passed_3()


if __name__ == "__main__":
    example6()
