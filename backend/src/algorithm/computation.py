from src.algorithm.equal_shares import equal_shares
from src.algorithm.utils import calculate_average_allocations, check_allocations, display_bar_chart, remove_zero_bids


def min_max_equal_shares(
    voters: list[int],
    cost_min_max: list[dict[int, tuple[int, int]]],
    budget: int,
    bids: dict[int, dict[int, int]],
) -> tuple[dict[int, int], dict[int, dict[int, float]]]:
    """
    The purpose of min_max_equal_shares function is to convert the input in the received format
    to a format suitable for the equal_shares function (Selects the minimum value)
        Args:
            voters (list): A list of voter names.
            projects (list): A list of project IDs.
            cost_min_max (dict): A dictionary mapping project IDs to their min and max costs.
            bids (dict): A dictionary mapping project IDs to the
            list of voters who approve them and the cost the voters chose.
            budget (int): The total budget available
        example:
            cost_min_max = [{1: (200, 700)}, {2: (300, 900)}, {3:(100,100)}] --> cost = [{1:200 }, {2:300}, {3:100}]
    """
    projects_min_costs = {project_id: min_value for d in cost_min_max for project_id, (min_value, _) in d.items()}
    # for item in cost_min_max:
    #     project_id, (min_value, _) = item.popitem()
    #     projects_min_costs[project_id] = min_value
    remove_zero_bids(bids)
    winners_allocations, candidates_payments_per_voter = equal_shares(voters, projects_min_costs, budget, bids)
    if not check_allocations(cost_min_max, winners_allocations):
        raise ValueError("the result is not valid")

    averages = calculate_average_allocations(winners_allocations, voters)
    display_bar_chart(cost_min_max, winners_allocations, averages)
    
    return winners_allocations, candidates_payments_per_voter

