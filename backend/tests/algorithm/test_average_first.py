import numpy as np

from src.algorithm.average_first import average_first
from src.algorithm.utils import calculate_average_bids


def test_average_first() -> None:
    voters = [1, 2]
    cost_min_max = [{11: (200, 500)}, {12: (300, 300)}, {13: (100, 150)}]
    bids = {11: {1: 500, 2: 200}, 12: {1: 300, 2: 300}, 13: {2: 100}}

    assert calculate_average_bids(bids, voters) == {11: 350.0, 12: 300.0, 13: 50.0}

    winners_allocations, _ = average_first(voters, cost_min_max, 900, bids, use_plt=False)
    assert {k: np.round(v) for k, v in winners_allocations.items()} == {11: 350, 12: 300, 13: 100}
