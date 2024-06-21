# this file only for test fixed_budget func

import logging
import doctest
logger = logging.getLogger("equal_shares_logger")


def find_max(bids: dict):
    '''
    #T.0
    >>> bids = { 1: {1: 100, 2: 100, 4: 100},2: {2: 150, 5: 150},3: {1: 200, 5: 200}, 4: {3: 250, 4: 250, },5: {2: 300, 3: 300, 5: 300},6: {2: 350, 5: 350}, 7: {1: 400, 4: 400, },8: {2: 450, 5: 450},9: {1: 500, 3: 500,5: 500},10:{2: 550, 3: 550}}
    >>> find_max(bids)
    {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    '''

    max_result = {key: 0 for key in bids}

    for project_id in bids:
        max_result[project_id] = max(bids[project_id].values(), default=0)  # Find the maximum value in the list

    return max_result




'''
This function accepts update_bids,update_approvers,curr_project_id,
budget_increment_per_project and curr_project_cost and returns all voters ​​in curr_project_id from update_bids,update_approvers
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


'''
def filter_bids(update_bids: dict, update_approvers: dict, curr_project_id: int, curr_project_cost: int, budget_increment_per_project: int,
                update_cost: dict):


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

    update_approvers[curr_project_id] = list(update_bids[curr_project_id].keys())




if __name__ == "__main__":
    import doctest

logger.setLevel(logging.WARNING)  # Turn off "info" log messages
print(doctest.testmod())
logger.setLevel(logging.INFO)  # Turn on "info" log messages
logger.addHandler(logging.StreamHandler())