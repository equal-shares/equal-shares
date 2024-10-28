from src.algorithm.equal_shares import equal_shares, equal_shares_fixed_budget
from src.algorithm.utils import find_max
import numpy as np


def test_equal_shares_passed() -> None:
    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {3: 250, 4: 250},
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {1: 400, 4: 400},
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500, 5: 500},
        20: {2: 550, 3: 550},
    }
    budget = 900  # Total budget
    winners_allocations, candidates_payments_per_voter = equal_shares(
        voters,
        projects_costs,
        budget,
        bids,
    )

    expected_winners_allocations = {11: 100, 12: 0, 13: 200, 14: 250, 15: 300, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
    expected_candidates_payments_per_voter: dict[int, dict[int, float]] = {
        11: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336},
        12: {2: 0, 5: 0},
        13: {1: 108.0, 5: 92.0},
        14: {3: 92.0, 4: 158.0},
        15: {2: 100.0, 3: 100.0, 5: 100.0},
        16: {2: 0, 5: 0},
        17: {1: 0, 4: 0},
        18: {2: 0, 5: 0},
        19: {1: 0, 3: 0, 5: 0},
        20: {2: 0, 3: 0},
    }

    assert {c: int(x) for c, x in winners_allocations.items()} == expected_winners_allocations

    compare_dicts(candidates_payments_per_voter, expected_candidates_payments_per_voter)


def test_equal_shares_fixed_budget_passed_1() -> None:
    """
    simple, no increment
    """

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {3: 250, 4: 250},
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {1: 400, 4: 400},
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500, 5: 500},
        20: {2: 550, 3: 550},
    }
    budget = 900

    max_bid_for_project = find_max(bids)
    winners_allocations, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    expected_winners_allocations = {11: 100, 12: 0, 13: 200, 14: 0, 15: 300, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}

    expected_updated_cost = {11: 0, 12: 150, 13: 0, 14: 250, 15: 0, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}

    expected_candidates_payments_per_voter = {
        11: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336},
        12: {2: 0, 5: 0},
        13: {1: 120.0, 5: 80.0},
        14: {3: 0, 4: 0},
        15: {2: 100.0, 3: 100.0, 5: 100.0},
        16: {2: 0, 5: 0},
        17: {1: 0, 4: 0},
        18: {2: 0, 5: 0},
        19: {1: 0, 3: 0, 5: 0},
        20: {2: 0, 3: 0},
    }

    assert {c: int(x) for c, x in winners_allocations.items()} == expected_winners_allocations
    assert updated_cost == expected_updated_cost

    compare_dicts(candidates_payments_per_voter, expected_candidates_payments_per_voter)


def test_equal_shares_fixed_budget_passed_2() -> None:
    """
    with increment in one project
    """

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {3: 250, 4: 250},
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {1: 400, 4: 400},
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500, 5: 500},
        20: {2: 550, 3: 550},
    }
    budget = 900

    bids[11][4] = 200

    max_bid_for_project = find_max(bids)
    winners_allocations, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    expected_winners_allocations = {11: 200, 12: 0, 13: 200, 14: 0, 15: 300, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
    expected_updated_cost = {11: 0, 12: 150, 13: 0, 14: 250, 15: 0, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    expected_candidates_payments_per_voter = {
        11: {1: 33.333333333333336, 2: 33.333333333333336, 4: 133.33333333333334},
        12: {2: 0, 5: 0},
        13: {1: 120.0, 5: 80.0},
        14: {3: 0, 4: 0},
        15: {2: 100.0, 3: 100.0, 5: 100.0},
        16: {2: 0, 5: 0},
        17: {1: 0, 4: 0},
        18: {2: 0, 5: 0},
        19: {1: 0, 3: 0, 5: 0},
        20: {2: 0, 3: 0},
    }

    assert {c: int(x) for c, x in winners_allocations.items()} == expected_winners_allocations
    assert updated_cost == expected_updated_cost

    compare_dicts(candidates_payments_per_voter, expected_candidates_payments_per_voter)


def test_equal_shares_fixed_budget_passed_3() -> None:
    """
    with increment in three projects
    """

    voters = [1, 2, 3, 4, 5]
    projects_costs = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {3: 250, 4: 250},
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {1: 400, 4: 400},
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500, 5: 500},
        20: {2: 550, 3: 550},
    }
    budget = 900

    bids[11][4] = 200

    bids[11][2] = 150
    bids[13][5] = 300
    bids[15][5] = 400
    bids[15][3] = 350

    max_bid_for_project = find_max(bids)
    winners_allocations, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    expected_winners_allocations = {11: 200, 12: 0, 13: 200, 14: 0, 15: 350, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
    expected_updated_cost = {11: 0, 12: 150, 13: 1, 14: 250, 15: 1, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    expected_candidates_payments_per_voter = {
        11: {1: 33.333333333333336, 2: 58.333333333333336, 4: 108.33333333333334},
        12: {2: 0, 5: 0},
        13: {1: 145.0, 5: 55.0},
        14: {3: 0, 4: 0},
        15: {2: 100.0, 3: 125.0, 5: 125.0},
        16: {2: 0, 5: 0},
        17: {1: 0, 4: 0},
        18: {2: 0, 5: 0},
        19: {1: 0, 3: 0, 5: 0},
        20: {2: 0, 3: 0},
    }

    assert {c: int(x) for c, x in winners_allocations.items()} == expected_winners_allocations
    assert updated_cost == expected_updated_cost

    compare_dicts(candidates_payments_per_voter, expected_candidates_payments_per_voter)


def test_equal_shares_fixed_budget_passed_4() -> None:
    """
    ensure that increment is fairly allocated
    """

    voters = [1, 2]
    projects_costs = {11: 100, 12: 100}
    bids = {11: {1: 200}, 12: {2: 200}}

    budget = 300

    max_bid_for_project = find_max(bids)
    winners_allocations, updated_cost, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, budget, bids, max_bid_for_project
    )

    expected_winners_allocations = {11: 150, 12: 150}
    expected_updated_cost = {11: 1, 12: 1}
    expected_candidates_payments_per_voter = {11: {1: 150.0}, 12: {2: 150.0}}

    assert {c: int(x) for c, x in winners_allocations.items()} == expected_winners_allocations
    assert updated_cost == expected_updated_cost

    compare_dicts(candidates_payments_per_voter, expected_candidates_payments_per_voter)


def compare_dicts(outcome: dict, expected: dict) -> None:
    assert outcome.keys() == expected.keys()
    for candidate, payments in outcome.items():
        for voter, _ in payments.items():
            assert np.round(outcome[candidate][voter]) == np.round(expected[candidate][voter])
