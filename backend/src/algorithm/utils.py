import matplotlib.pyplot as plt
import numpy as np

import logging
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



def remove_zero_bids(bids):
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


def check_allocations(cost_min_max, winners_allocations):

    """ 
    Inputs:

    cost_min_max is a list of dictionaries where each key is associated with a tuple containing the minimum and maximum costs.
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
                    logger.info(f"project_cost {project_cost} for project_id {project_id} is NOT within the range {min_cost}-{max_cost}.")                            
            else:
                continue
    return boll_flag 


def calculate_average_allocations(winners_allocations, voters):
    """
    Inputs:
    winners_allocations: A dictionary where each key represents a winner's allocation value.
    voters: A list of voters whose size will be used to divide the allocations.
    Function:

    The function first checks the size of the voters list and ensures that it is greater than zero to avoid division by zero.
    For each key in winners_allocations, it divides the allocation value by the number of voters and prints the result.
    The results are stored in a dictionary called averages, which is returned by the function.
    
    """
    # Get the number of voters
    num_voters = len(voters)
    
    # Check if the number of voters is greater than zero to avoid division by zero
    if num_voters == 0:
        print("Error: The voters list is empty. Division by zero is not possible.")
        return

    # Calculate the average for each project_cost in winners_allocations
    averages = {}
    for project_id, project_cost in winners_allocations.items():
        average = project_cost / num_voters
        averages[project_id] = average
        logger.info(f"Average allocation for project_id {project_id}: {average}")

    return averages



def display_bar_chart(cost_min_max, winners_allocations, averages):\
    pass
