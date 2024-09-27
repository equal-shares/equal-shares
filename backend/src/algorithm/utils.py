import logging

import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger("equal_shares_logger")


def find_max(bids: dict[int, dict[int, int]]) -> dict[int, int]:
    max_result = {key: 0 for key in bids}

    for project_id in bids:
        max_result[project_id] = max(bids[project_id].values(), default=0)  # Find the maximum value in the list

    return max_result


"""

   Args:
        update_bids (dict): A dictionary mapping project IDs to the
        list of voters who approve them and the cost the voters chose.
        update_approvers (list): A list of project IDs.
        curr_project_id (int): The id number of current project
        curr_project_cost (int): The cost of current project
        budget_increment_per_project (int) : A const number marking the steps between the maximum and minimum price
        update_cost (dict): A dictionary mapping project IDs to their current costs.

This void function accepts this Args and returns all voters ​​in curr_project_id from update_bids,update_approvers
that their budget vote are greater or equal than curr_project_cost.
In addition, filter_bids update update_cost to be at budget_increment_per_project price

example 1:

input:                                  -->  output/ update this value after call filter bids

update_bids: {1: {2: 99}, 2: {1: 98}}   --> {1: {2: 99}, 2: {}}
update_approvers: {1: [2], 2: [1]}      --> {1: [2], 2: []}
curr_project_id: 2                      --> 2
curr_project_cost: 98                   --> 98
budget_increment_per_project: 10        --> 10
update_cost: {1: 99, 2: 98}             --> {1: 99, 2: 10}


example 1:

input:                                  -->  output/ update this value after call filter bids

update_bids:
{1: {1: 100, 2: 130, 4: 150},           --> {1: {2: 30, 4: 50},
2: {2: 160, 5: 190},                    --> 2: {2: 160, 5: 190},
3: {1: 200, 5: 240},                    --> 3: {1: 200, 5: 240},
4: {3: 270, 4: 280},                    --> 4: {3: 270, 4: 280},
5: {2: 310, 3: 320, 5: 340},            --> 5: {2: 310, 3: 320, 5: 340},
6: {2: 360, 5: 390},                    --> 6: {2: 360, 5: 390},
7: {1: 400, 4: 430},                    --> 7: {1: 400, 4: 430},
8: {2: 460, 5: 490},                    --> 8: {2: 460, 5: 490},
9: {1: 500, 3: 520, 5: 540},            --> 9: {1: 500, 3: 520, 5: 540},
10: {2: 560, 3: 570}}                   --> 10: {2: 560, 3: 570}}

update_approvers
{1: [1, 2, 4], 2: [2, 5],               --> {1: [2, 4], 2: [2, 5],
3: [1, 5], 4: [3, 4],                   --> 3: [1, 5], 4: [3, 4],
5: [2, 3, 5], 6: [2, 5],                --> 5: [2, 3, 5], 6: [2, 5],
7: [1, 4], 8: [2, 5],                   --> 7: [1, 4], 8: [2, 5],
9: [1, 3, 5], 10: [2, 3]}               --> 9: [1, 3, 5], 10: [2, 3]}

curr_project_id: 1                      --> 1
curr_project_cost: 100                  --> 100
budget_increment_per_project: 10        --> 10
update_cost:
{1: 100, 2: 150, 3: 200, 4: 250, 5: 300,  --> {1: 10, 2: 150, 3: 200, 4: 250, 5: 300,
6: 350, 7: 400, 8: 450, 9: 500, 10: 550}  --> 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}


"""


def filter_bids(
    update_bids: dict[int, dict[int, int]],
    curr_project_id: int,
    curr_project_cost: int,
    budget_increment_per_project: int,
    update_cost: dict[int, int],
) -> None:
    if curr_project_id in update_bids:
        voters_to_remove = []
        for voter_id, price in update_bids[curr_project_id].items():
            update_project_price = price - (curr_project_cost + budget_increment_per_project)  # for the next iteration
            if update_project_price < 0:
                voters_to_remove.append(voter_id)
                update_cost[curr_project_id] = budget_increment_per_project
            else:
                update_bids[curr_project_id][voter_id] = update_project_price + budget_increment_per_project
                update_cost[curr_project_id] = budget_increment_per_project

        for voter_id in voters_to_remove:
            update_bids[curr_project_id].pop(voter_id)


def remove_zero_bids(bids: dict[int, dict[int, int]]) -> dict[int, dict[int, int]]:
    """
    This function loops through each bid's internal dictionary and
    creates a new dictionary excluding any key-value pairs where the value is 0.
    It then updates the original dictionary with the cleaned version.
    example:
    input:  bids = {1: {1: 70000, 2: 0, 3: 44000, 4: 0, 5: 28000, 6: 11000, 7: 0, 8: 11000, 9: 20000}}
    output: bids = {1: {1: 70000, 3: 44000, 5: 28000, 6: 11000, 8: 11000, 9: 20000}}
    """
    # Iterate through the main dictionary
    for project, sub_dict in bids.items():
        # Create a new dictionary by excluding entries with value 0
        bids[project] = {voter_id: voter_cost for voter_id, voter_cost in sub_dict.items() if voter_cost != 0}
    return bids


def check_allocations(cost_min_max: list[dict[int, tuple[int, int]]], winners_allocations: dict[int, int]) -> bool:
    """
    Inputs:

    cost_min_max is a list of dictionaries where each key is associated
    with a tuple containing the minimum and maximum costs.
    winners_allocations is a dictionary where each key represents an allocation value.
    Function:

    The function iterates through each key-value pair in winners_allocations.
    If the allocation is not zero, it searches for the corresponding range in cost_min_max.
    If found, it checks whether the allocation falls within the specified range and prints the result.

    """

    boll_flag = True
    # Loop through each key and value in winners_allocations
    for project_id, project_cost in winners_allocations.items():
        # Check if the project_cost is not zero
        if project_cost != 0:
            # Find the corresponding range in cost_min_max
            cost_range = next((entry[project_id] for entry in cost_min_max if project_cost in entry), None)

            if cost_range:
                min_cost, max_cost = cost_range
                # Check if the project_cost falls within the range
                if not min_cost <= project_cost <= max_cost:
                    boll_flag = False
                    logger.info(
                        f"project_cost {project_cost} for project_id {project_id} "
                        f"is NOT within the range {min_cost}-{max_cost}."
                    )
            else:
                continue
    return boll_flag


def calculate_average_bids(bids: dict[int, dict[int, int]], voters: list[int]) -> dict[int, float]:
    """
    Function to calculate the average of bids for each project.

    Args:
    bids (dict): A dictionary where the keys are project IDs and the values are dictionaries of voter bids.
    len(voters) = N (int): The number to divide the sum of bids for each project.

    Returns:
    dict: A dictionary where the keys are project IDs and the values are the average bids.
    """
    average_bids = {}
    N = len(voters)
    for project_id, voter_bids in bids.items():
        total_sum = sum(voter_bids.values())  # Sum all bids for the project
        average_bids[project_id] = total_sum / N  # Divide by N and store in the dictionary

    return average_bids


def plot_bid_data(
    bids: dict[int, dict[int, int]],
    cost_min_max: list[dict[int, tuple[int, int]]],
    average_bids: dict[int, float],
    winners_allocations: dict[int, int],
) -> None:
    # Extracting project IDs
    project_ids = list(bids.keys())

    # Flattening cost_min_max to work with the list of dictionaries
    cost_min_values = []
    cost_max_values = []
    for project_id in project_ids:
        for cost_dict in cost_min_max:
            if project_id in cost_dict:
                cost_min, cost_max = cost_dict[project_id]
                cost_min_values.append(cost_min)
                cost_max_values.append(cost_max)
                break

    # Extracting values for average_bids and winners_allocations
    avg_bids_values = [average_bids[pid] for pid in project_ids]
    winners_allocations_values = [winners_allocations[pid] for pid in project_ids]

    # Bar width
    bar_width = 0.5
    x_pos = np.arange(len(project_ids))

    # Small offset for equal values
    small_offset = 0.001

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Sort the values (Average Bids, Winners Allocations, Cost Min, Cost Max) per project in ascending order
    for i, project_id in enumerate(project_ids):
        values = [
            ("Average Bids", avg_bids_values[i], "blue"),
            ("Winners Allocations", winners_allocations_values[i], "green"),
            ("Cost Min", cost_min_values[i], "red"),
            ("Cost Max", cost_max_values[i], "orange"),
        ]

        # Sort the values by the second element (the value itself)
        values_sorted = sorted(values, key=lambda x: x[1])

        # Plot the sorted bars, applying a small horizontal offset to distinguish equal values
        cumulative_bottom = 0.0
        last_value = None
        for label, value, color in values_sorted:
            if last_value is not None and value == last_value:
                # Add small horizontal offset for equal values
                value += small_offset
            plt.bar(
                x_pos[i], value, width=bar_width, label=label if i == 0 else "", color=color, bottom=cumulative_bottom
            )
            cumulative_bottom += value
            last_value = value

    # Adding labels and title
    plt.xlabel("Project ID")
    plt.ylabel("Value")
    plt.title("Bids, Winners Allocations, and Costs for Projects (Sorted and Offset for Equal Values)")
    plt.xticks(x_pos, [str(item) for item in project_ids])
    plt.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()
