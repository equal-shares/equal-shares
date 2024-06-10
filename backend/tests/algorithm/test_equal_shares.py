from src.algorithm.equal_shares import equal_shares, equal_shares_fixed_budget


def test_equal_shares_passed() -> None:
    voters = [1, 2, 3, 4, 5]  # Voters
    projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    cost = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    approvers = {
        1: [1, 2, 4],
        2: [2, 5],
        3: [1, 5],
        4: [3, 4],
        5: [2, 3, 5],
        6: [2, 5],
        7: [1, 4],
        8: [2, 5],
        9: [1, 3, 5],
        10: [2, 3],
    }
    bids = {
        1: {1: 100, 2: 100, 4: 100},
        2: {2: 150, 5: 150},
        3: {1: 200, 5: 200},
        4: {
            3: 250,
            4: 250,
        },
        5: {2: 300, 3: 300, 5: 300},
        6: {2: 350, 5: 350},
        7: {
            1: 400,
            4: 400,
        },
        8: {2: 450, 5: 450},
        9: {1: 500, 3: 500, 5: 500},
        10: {2: 550, 3: 550},
    }
    budget = 900  # Total budget
    budget_increment_per_project = 10

    res = equal_shares(voters, projects, cost, approvers, budget, bids, budget_increment_per_project)

    exected = (
        [1, 3, 4, 5],
        {1: 100, 2: 0, 3: 200, 4: 250, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
        {
            1: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336},
            2: {2: 0, 5: 0},
            3: {1: 108.0, 5: 0},
            4: {3: 0, 4: 158.0},
            5: {2: 100.0, 3: 100.0, 5: 100.0},
            6: {2: 0, 5: 0},
            7: {1: 0, 4: 0},
            8: {2: 0, 5: 0},
            9: {1: 0, 3: 0, 5: 0},
            10: {2: 0, 3: 0},
        },
    )

    assert isinstance(res, tuple)
    assert len(res) == len(exected)
    assert res[0] == exected[0]
    assert res[1] == exected[1]
    assert res[2] == exected[2]


def test_equal_shares_fixed_budget_passed() -> None:
    voters = [1, 2, 3, 4, 5]  # Voters
    projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    cost = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    approvers = {
        1: [1, 2, 4],
        2: [2, 5],
        3: [1, 5],
        4: [3, 4],
        5: [2, 3, 5],
        6: [2, 5],
        7: [1, 4],
        8: [2, 5],
        9: [1, 3, 5],
        10: [2, 3],
    }
    bids = {
        1: {1: 100, 2: 100, 4: 100},
        2: {2: 150, 5: 150},
        3: {1: 200, 5: 200},
        4: {
            3: 250,
            4: 250,
        },
        5: {2: 300, 3: 300, 5: 300},
        6: {2: 350, 5: 350},
        7: {
            1: 400,
            4: 400,
        },
        8: {2: 450, 5: 450},
        9: {1: 500, 3: 500, 5: 500},
        10: {2: 550, 3: 550},
    }
    budget = 900  # Total budget
    budget_increment_per_project = 10
    max_cost_for_project = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}

    res = equal_shares_fixed_budget(
        voters, projects, cost, approvers, budget, bids, budget_increment_per_project, max_cost_for_project
    )

    exected = (
        [1, 3, 5],
        {1: 100, 2: 0, 3: 200, 4: 0, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},
        {1: 10, 2: 150, 3: 10, 4: 250, 5: 10, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550},
        {
            1: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336},
            2: {2: 0, 5: 0},
            3: {1: 120.0, 5: 0},
            4: {3: 0, 4: 0},
            5: {2: 100.0, 3: 100.0, 5: 100.0},
            6: {2: 0, 5: 0},
            7: {1: 0, 4: 0},
            8: {2: 0, 5: 0},
            9: {1: 0, 3: 0, 5: 0},
            10: {2: 0, 3: 0},
        },
    )

    assert isinstance(res, tuple)
    assert len(res) == len(exected)
    assert res[0] == exected[0]
    assert res[1] == exected[1]
    assert res[2] == exected[2]
