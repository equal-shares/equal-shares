from src.algorithm.computation import min_max_equal_shares


def test_min_max_equal_shares_passed_1() -> None:
    """
    Testing of multiple projects
    """

    voters = [1, 2, 3, 4, 5]
    projects_costs = [
        {11: (100, 200)},
        {12: (150, 250)},
        {13: (200, 300)},
        {14: (250, 350)},
        {15: (300, 400)},
        {16: (350, 450)},
        {17: (400, 500)},
        {18: (450, 550)},
        {19: (500, 600)},
        {20: (550, 650)},
    ]
    bids = {
        11: {1: 100, 2: 130, 4: 150},
        12: {2: 160, 5: 190},
        13: {1: 200, 5: 240},
        14: {3: 270, 4: 280},
        15: {2: 310, 3: 320, 5: 340},
        16: {2: 360, 5: 390},
        17: {1: 400, 4: 430},
        18: {2: 460, 5: 490},
        19: {1: 500, 3: 520, 5: 540},
        20: {2: 560, 3: 570},
    }
    budget = 900

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 150, 12: 0, 13: 200, 14: 0, 15: 320, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}
    expected_candidates_payments_per_voter = {
        11: {1: 33.333333333333336, 2: 48.333333333333336, 4: 68.33333333333334},
        12: {2: 0, 5: 0},
        13: {1: 105.33333333333333, 5: 94.66666666666667},
        14: {3: 0, 4: 0},
        15: {2: 103.33333333333333, 3: 108.33333333333333, 5: 108.33333333333333},
        16: {2: 0, 5: 0},
        17: {1: 0, 4: 0},
        18: {2: 0, 5: 0},
        19: {1: 0, 3: 0, 5: 0},
        20: {2: 0, 3: 0},
    }

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_2() -> None:
    """
    Three projects with different prices
    """

    voters = [1, 2]
    projects_costs = [{11: (200, 700)}, {12: (300, 900)}, {13: (100, 100)}]
    bids = {11: {1: 500, 2: 200}, 12: {1: 300, 2: 300}, 13: {2: 100}}
    budget = 900

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 500, 12: 300, 13: 100}
    expected_candidates_payments_per_voter = {11: {1: 400.0, 2: 100.0}, 12: {1: 150.0, 2: 150.0}, 13: {2: 100.0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_3() -> None:
    """
    Two projects with the same amount of voters and the price difference between them is 1
    """

    voters = [1, 2]
    projects_costs = [{11: (99, 200)}, {12: (98, 200)}]
    bids = {11: {2: 99}, 12: {1: 98}}
    budget = 100

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 0, 12: 98}
    expected_candidates_payments_per_voter = {11: {2: 0}, 12: {1: 98.0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_4() -> None:
    """
    For 4 projects with same cost and same voters,
    while the budget suffices for all the 1 ( take the first index)
    """

    voters = [1, 2, 3, 4]
    projects_costs = [{11: (500, 600)}, {12: (500, 600)}, {13: (500, 600)}, {14: (500, 600)}]
    bids = {
        11: {1: 500, 2: 500, 3: 500, 4: 500},
        12: {1: 500, 2: 500, 3: 500, 4: 500},
        13: {1: 500, 2: 500, 3: 500, 4: 500},
        14: {1: 500, 2: 500, 3: 500, 4: 500},
    }
    budget = 500

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 500, 12: 0, 13: 0, 14: 0}
    expected_candidates_payments_per_voter = {
        11: {1: 125.0, 2: 125.0, 3: 125.0, 4: 125.0},
        12: {1: 0, 2: 0, 3: 0, 4: 0},
        13: {1: 0, 2: 0, 3: 0, 4: 0},
        14: {1: 0, 2: 0, 3: 0, 4: 0},
    }

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_5() -> None:
    """
    For one projects with one voter. the budget > project cost.
    """

    voters = [1]
    projects_costs = [{11: (500, 600)}]
    bids = {11: {1: 600}}
    budget = 1000

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 600}
    expected_candidates_payments_per_voter = {11: {1: 600.0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_6() -> None:
    """
    For one projects with one voter. the budget <= project min cost.
    """

    voters = [1]
    projects_costs = [{11: (500, 600)}]
    bids = {11: {1: 600}}
    budget = 500

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 500}
    expected_candidates_payments_per_voter = {11: {1: 500.0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_7() -> None:
    """
    For one projects with one voter. the budget < project min  cost.
    """

    voters = [1]
    projects_costs = [{11: (600, 600)}]
    bids = {11: {1: 600}}
    budget = 500

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_winners_allocations = {11: 0}
    expected_candidates_payments_per_voter = {11: {1: 0}}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]


def test_min_max_equal_shares_passed_8() -> None:
    """
    For 3 projects with same cost and same voters, while the budget suffices for all the 3 .
    """

    voters = [1, 2, 3]
    projects_costs = [{11: (500, 600)}, {12: (500, 600)}, {13: (500, 600)}]
    bids = {11: {1: 500, 2: 500, 3: 500}, 12: {1: 500, 2: 500, 3: 500}, 13: {1: 500, 2: 500, 3: 500}}
    budget = 1500

    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, projects_costs, budget, bids)

    expected_candidates_payments_per_voter = {
        11: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666},
        12: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666},
        13: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666},
    }
    expected_winners_allocations = {11: 500, 12: 500, 13: 500}

    assert winners_allocations == expected_winners_allocations

    assert candidates_payments_per_voter.keys() == expected_candidates_payments_per_voter.keys()
    for key in candidates_payments_per_voter:
        assert candidates_payments_per_voter[key] == expected_candidates_payments_per_voter[key]
