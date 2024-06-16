import logging

from equal_shares import equal_shares

logger = logging.getLogger("equal_shares_logger")


def min_max_equal_shares(voters, projects, cost_min_max, bids, budget, budget_increment_per_project):
    """
    T.0
    >>> voters = [1, 2, 3, 4, 5]  # Voters
    >>> projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    >>> cost = [
    ...     {1: (100, 200)},
    ...     {2: (150, 250)},
    ...     {3: (200, 300)},
    ...     {4: (250, 350)},
    ...     {5: (300, 400)},
    ...     {6: (350, 450)},
    ...     {7: (400, 500)},
    ...     {8: (450, 550)},
    ...     {9: (500, 600)},
    ...     {10: (550, 650)}
    ... ]
    >>> bids = {
    ...     1: {1: 100, 2: 130, 4: 150},
    ...     2: {2: 160, 5: 190},
    ...     3: {1: 200, 5: 240},
    ...     4: {3: 270, 4: 280},
    ...     5: {2: 310, 3: 320, 5: 340},
    ...     6: {2: 360, 5: 390},
    ...     7: {1: 400, 4: 430},
    ...     8: {2: 460, 5: 490},
    ...     9: {1: 500, 3: 520, 5: 540},
    ...     10:{2: 560, 3: 570}
    ... }
    >>> budget = 900  # Total budget
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects, cost, bids, budget,budget_increment_per_project)
    ([1, 3, 4, 5], {1: 100, 2: 0, 3: 200, 4: 250, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, {1: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336}, 2: {2: 0, 5: 0}, 3: {1: 108.0, 5: 0}, 4: {3: 0, 4: 158.0}, 5: {2: 100.0, 3: 100.0, 5: 100.0}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0}, 8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}})
    """

    # """
    # T.0
    # >>> voters = [1, 2, 3, 4, 5]  # Voters
    # >>> projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    # >>> cost = [
    # ...     {1: (100, 200)},
    # ...     {2: (150, 250)},
    # ...     {3: (200, 300)},
    # ...     {4: (250, 350)},
    # ...     {5: (300, 400)},
    # ...     {6: (350, 450)},
    # ...     {7: (400, 500)},
    # ...     {8: (450, 550)},
    # ...     {9: (500, 600)},
    # ...     {10: (550, 650)}
    # ... ]
    # >>> bids = {
    # ...     1: {1: 100, 2: 130, 4: 150},
    # ...     2: {2: 160, 5: 190},
    # ...     3: {1: 200, 5: 240},
    # ...     4: {3: 270, 4: 280},
    # ...     5: {2: 310, 3: 320, 5: 340},
    # ...     6: {2: 360, 5: 390},
    # ...     7: {1: 400, 4: 430},
    # ...     8: {2: 460, 5: 490},
    # ...     9: {1: 500, 3: 520, 5: 540},
    # ...     10:{2: 560, 3: 570}
    # ... }
    # >>> budget = 900  # Total budget
    # >>> budget_increment_per_project = 10
    # >>> min_max_equal_shares(voters, projects, cost, bids, budget,budget_increment_per_project)
    # ([1, 3, 4, 5],\
    # {1: 100, 2: 0, 3: 200, 4: 250, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0},\
    # {\
    #     1: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336},\
    #     2: {2: 0, 5: 0}, 3: {1: 108.0, 5: 0}, 4: {3: 0, 4: 158.0},\
    #     5: {2: 100.0, 3: 100.0, 5: 100.0}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0},\
    #     8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}\
    # })
    # """

    cost = {}
    for item in cost_min_max:
        project_id, (min_value, _) = item.popitem()
        cost[project_id] = min_value

    approvers = {}
    for project_id, value in bids.items():
        approvers[project_id] = list(value.keys())

    return equal_shares(voters, projects, cost, approvers, budget, bids, budget_increment_per_project)

if __name__=="__main__":
    import doctest
    print(doctest.testmod())
