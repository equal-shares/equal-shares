# computation.py
from equal_shares import equal_shares
import logging
import doctest
logger = logging.getLogger("equal_shares_logger")


"""
 The purpose of min_max_equal_shares function is to convert the input in the received format
 to a format suitable for the equal_shares function (Selects the minimum value)
   
   
   
   Args:
        voters (list): A list of voter names.
        projects (list): A list of project IDs.
        cost_min_max (dict): A dictionary mapping project IDs to their min and max costs.
        bids (dict): A dictionary mapping project IDs to the list of voters who approve them and the cost the voters chose.
        budget (int): The total budget available
        budget_increment_per_project (int) : A const number marking the steps between the maximum and minimum price
        
 example: 
        cost_min_max = [{1: (200, 700)}, {2: (300, 900)}, {3:(100,100)}] --> cost = [{1:200 }, {2:300}, {3:100}]

 
"""



def min_max_equal_shares(voters:list, projects: list, cost_min_max: dict, bids: dict, budget: int, budget_increment_per_project: int):


    '''
    # T.0 Testing of multiple projects

    >>> voters = [1, 2, 3, 4, 5]  
    >>> projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    >>> cost = [{1: (100, 200)}, {2: (150, 250)}, {3: (200, 300)}, {4: (250, 350)}, {5: (300, 400)},{6: (350, 450)}, {7: (400, 500)}, {8: (450, 550)}, {9: (500, 600)}, {10: (550, 650)}]
    >>> bids = { 1: {1: 100, 2: 130, 4: 150},2: {2: 160, 5: 190},3: {1: 200, 5: 240}, 4: {3: 270, 4: 280, },5: {2: 310, 3: 320, 5: 340},6: {2: 360, 5: 390}, 7: {1: 400, 4: 430, },8: {2: 460, 5: 490},9: {1: 500, 3: 520,5: 540},10:{2: 560, 3: 570}}
    >>> budget = 900 
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects, cost, bids, budget,budget_increment_per_project)
    ([1, 3, 4, 5], {1: 130, 2: 0, 3: 200, 4: 250, 5: 320, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, {1: {1: 33.333333333333336, 2: 48.333333333333336, 4: 48.333333333333336}, 2: {2: 0, 5: 0}, 3: {1: 104.33333333333333, 5: 0}, 4: {3: 0, 4: 154.33333333333331}, 5: {2: 103.33333333333333, 3: 108.33333333333333, 5: 108.33333333333333}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0}, 8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}})
    
    #T.1 Three projects with different prices

    >>> voters = [1, 2]  # voter
    >>> projects = [1, 2, 3]  # Project IDs
    >>> cost = [{1: (200, 700)}, {2: (300, 900)}, {3:(100,100)}]
    >>> bids = {1: {1: 500, 2:200}, 2: {1: 300, 2: 300} ,3:{2:100}}
    >>> budget = 900  
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects, cost, bids, budget, budget_increment_per_project)
    ([1, 2, 3], {1: 500, 2: 300, 3: 100}, {1: {1: 390.0, 2: 100.0}, 2: {1: 150.0, 2: 150.0}, 3: {2: 100.0}})
   
    #T.2 Two projects with the same amount of voters and the price difference between them is 1
    >>> voters = [1, 2]  # voter
    >>> projects = [1, 2]  # Project IDs
    >>> cost =  [{1: (99, 200)}, {2: (98, 200)}]
    >>> bids = {1: {2:99}, 2: {1:98}}
    >>> budget = 100  
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects, cost, bids, budget, budget_increment_per_project)
    ([2], {1: 0, 2: 98}, {1: {2: 0}, 2: {1: 0}})
    
    
    # T.3 For 4 projects with same cost and same voters, while the budget suffices for all the 1 ( take the first index) .
    >>> voters = [1, 2, 3, 4]  # voter
    >>> projects = [1, 2, 3, 4]  # Project IDs
    >>> cost = [{1: (500, 600)}, {2: (500, 600)}, {3: (500, 600)}, {4: (500, 600)}]
    >>> bids = {1: {1: 500, 2: 500 ,3: 500, 4: 500 }, 2: {1: 500, 2: 500 ,3: 500, 4: 500 }, 3: {1: 500, 2: 500 ,3: 500, 4: 500 }, 4: {1: 500, 2: 500 ,3: 500, 4: 500 }}  # for each project
    >>> budget = 500  # Total budget
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects, cost, bids, budget, budget_increment_per_project)
    ([1], {1: 500, 2: 0, 3: 0, 4: 0}, {1: {1: 0, 2: 0, 3: 0, 4: 0}, 2: {1: 0, 2: 0, 3: 0, 4: 0}, 3: {1: 0, 2: 0, 3: 0, 4: 0}, 4: {1: 0, 2: 0, 3: 0, 4: 0}})
    
    
    # # T.4 For one projects with one voter. the budget > project cost.
    # >>> voters = [1]  # voter
    # >>> projects = [1]  # Project IDs
    # >>> cost = [{1: (500, 600)}]  # Cost for each project
    # >>> bids = {1: {1: 600}}  # Approvers for each project
    # >>> budget = 1000  # Budget
    # >>> budget_increment_per_project = 10
    # >>> min_max_equal_shares(voters, projects, cost, bids, budget,budget_increment_per_project)
    ([1], {1: 600}, {1: {1: 600.0}})    #
    

    # T.5 For one projects with one voter. the budget <= project min cost.
    #>>> voters = [1]  
    #>>> projects = [1] 
    #>>> cost = [{1: (500, 600)}]  # Cost for each project
    #>>> bids = {1: {1: 600}}  # Approvers for each project
    #>>> budget = 500  
    #>>> budget_increment_per_project = 10
    ([1], {1: 500}, {1: {1: 0}})
    
    # # T.6 For one projects with one voter. the budget < project min  cost.
    #>>> voters = [1] 
    #>>> projects = [1]  
    #>>> cost = [{1: (600, 600)}]  # Cost for each project
    #>>> bids = {1: {1: 600}}
    #>>> budget = 500 
    #>>> budget_increment_per_project = 10
    ([], {1: 0}, {1: {1: 0}}

    # # T.7  For 3 projects with same cost and same voters, while the budget suffices for all the 3 .
    >>> voters = [1, 2, 3]  # voter
    >>> projects = [1, 2 ,3 ]  # Project IDs
    >>> cost = [{1: (500, 600)}, {2:  (500, 600)}, {3:  (500, 600)}]
    >>> bids = {1: {1: 500, 2: 500, 3: 500}, 2: {1: 500, 2: 500, 3: 500} , 3: {1: 500, 2: 500, 3: 500}}   #  for each project
    >>> budget = 1500                 # Total budget
    >>> budget_increment_per_project = 10
    >>> min_max_equal_shares(voters, projects,cost,bids,budget,budget_increment_per_project)
    ([1, 2, 3], {1: 500, 2: 500, 3: 500}, {1: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666}, 2: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666}, 3: {1: 166.66666666666666, 2: 166.66666666666666, 3: 166.66666666666666}})
    '''



    cost = {}
    for item in cost_min_max:
        project_id, (min_value, _) = item.popitem()
        cost[project_id] = min_value

    approvers = {}
    for project_id, value in bids.items():
        approvers[project_id] = list(value.keys())

    return equal_shares(voters, projects, cost, approvers, budget, bids, budget_increment_per_project)


if __name__ == "__main__":
    import time

    logger.setLevel(logging.WARNING)  # Turn off "info" log messages
    print(doctest.testmod())
    logger.setLevel(logging.INFO)  # Turn on "info" log messages
    logger.addHandler(logging.StreamHandler())

