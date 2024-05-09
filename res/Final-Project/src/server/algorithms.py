"""
This file contains the algorithms that will be used in the project for calculating the budget.
"""
import concurrent.futures
import logging
import statistics

import numpy as np
from counter import Counter
from tree import Tree

__all__ = [
    "median_algorithm",
    "generalized_median_algorithm",
    "calculate_totals",
    "update_dict_ids",
    "convert_structure",
    "unite_votes",
]

def median_algorithm(votes: dict) -> dict:
    """
    Calculate the median of the votes for the budget and return the budget according to the median votes.

    Args
    ----
    votes (dict): A nested dictionary representing the votes of all citizens for the budget.

    Returns
    -------
    final_budget (dict): A nested dictionary representing the budget according to the median votes of all citizens.

    References
    ----------
    https://en.wikipedia.org/wiki/Median

    Example
    -------
    >>> votes = {
    ...     "user1": {
    ...         "Department of Defense": {
    ...             "Army": 40,
    ...             "Police": 30,
    ...             "total": 70
    ...         },
    ...         "Department of Education": {
    ...             "Schools": 20,
    ...             "Higher education": 10,
    ...             "total": 30
    ...         },
    ...         "total": 100
    ...     },
    ...     "user2": {
    ...         "Department of Defense": {
    ...             "Army": 10,
    ...             "Police": 10,
    ...             "total": 20
    ...         },
    ...         "Department of Education": {
    ...             "Schools": 30,
    ...             "Higher education": 50,
    ...             "total": 80
    ...         },
    ...         "total": 100
    ...     }
    ... }

    >>> budget_data = median_algorithm(votes)

    >>> budget_data == {
    ...     "Department of Defense": {
    ...         "Army": 25,
    ...         "Police": 20,
    ...         "total": 45
    ...     },
    ...     "Department of Education": {
    ...         "Schools": 25,
    ...         "Higher education": 30,
    ...         "total": 55
    ...     },
    ...         "total": 100
    ... }
    True
    """

    final_budget = _run_algorithm(votes, 1)

    return final_budget


def generalized_median_algorithm(votes: dict) -> dict:
    """
    Calculate the budget according to the median algorithm of Hervé Moulin, using linear functions by using the given votes.

    Args
    ----
    votes (dict): A nested dictionary representing the votes of all citizens for the budget.

    Returns
    -------
    final_budget (dict): A nested dictionary representing the budget according to the median algorithm of Hervé Moulin.

    References
    ----------
    Hervé Moulin. "Fair Division and Collective Welfare". MIT Press, 2003.

    Example
    -------
    >>> votes = {
    ...     "user1": {
    ...         "Department of Defense": {
    ...             "Army": 2,
    ...             "total": 2
    ...         },
    ...         "Department of Education": {
    ...             "Schools": 0,
    ...             "total": 0
    ...         },
    ...         "Department of Interior": {
    ...             "immigration": 0,
    ...             "total": 0
    ...         },
    ...         "total": 2
    ...     },
    ...     "user2": {
    ...         "Department of Defense": {
    ...             "Army": 0,
    ...             "total": 0
    ...         },
    ...         "Department of Education": {
    ...             "Schools": 1,
    ...             "total": 1
    ...         },
    ...         "Department of Interior": {
    ...             "immigration": 1,
    ...             "total": 1
    ...         },
    ...         "total": 2
    ...     },
    ...     "user3": {
    ...         "Department of Defense": {
    ...             "Army": 1,
    ...             "total": 1
    ...         },
    ...         "Department of Education": {
    ...             "Schools": 1,
    ...             "total": 1
    ...         },
    ...         "Department of Interior": {
    ...             "immigration": 0,
    ...             "total": 0
    ...         },
    ...         "total": 2
    ...     }
    ... }

    >>> budget_data = generalized_median_algorithm(votes)

    >>> budget_data == {
    ...     "Department of Defense": {
    ...         "Army": 0.8,
    ...         "total": 0.8
    ...     },
    ...     "Department of Education": {
    ...         "Schools": 0.8,
    ...         "total": 0.8
    ...     },
    ...     "Department of Interior": {
    ...         "immigration": 0.4,
    ...         "total": 0.4
    ...     },
    ...     "total": 2
    ... }
    True
    """

    final_budget = _run_algorithm(votes, 2)

    return final_budget


def calculate_totals(node: dict) -> int:
    """
    Recursively calculates the total value of a nested dictionary by summing up all the values of keys named "allocated_budget_amount".
    The function also adds "allocated_budget_amount" keys to the dictionary at each level,
    with the value being the sum of all the "allocated_budget_amount" values of its sub-levels.

    Args:
        node (dict): A dictionary representing a node in a tree structure.

    Returns:
        int: The total allocated budget amount for the given node and its descendants.
    """
    allocated_budget_amount = 0

    # if the allocated_budget_amount is an integer or float, add it to the allocated_budget_amount variable
    # otherwise, set the allocated_budget_amount for this node to 0
    if isinstance(node["allocated_budget_amount"], (int, float)):
        allocated_budget_amount += node["allocated_budget_amount"]
    else:
        node["allocated_budget_amount"] = 0

    # for each child of the current node, recursively call the _calculate_totals function to calculate
    # the total allocated budget amount for the child, and add it to the allocated_budget_amount of the current node
    for child in node["children"]:
        child_budget_amount = calculate_totals(child)
        node["allocated_budget_amount"] += child_budget_amount

    # return the allocated_budget_amount of the current node and its descendants
    return node["allocated_budget_amount"]


def update_dict_ids(counter: Counter, input_dict: dict, parent_id=None):
    """
    Recursively updates the 'id' and 'parent' values of a dictionary to make them unique and in incremental order.

    Args:
        input_dict (dict): Input dictionary to update.
        parent_id (int): Parent id to set for the children. Default is None.
        current_id (int): Current id to use for updating the dictionary. Default is 0.

    Returns:
        dict: Updated dictionary with unique and incremental 'id' and 'parent' values.
    """
    input_dict["id"] = counter.current_id
    input_dict["parent"] = parent_id

    children = input_dict.get("children", [])
    num_children = len(children)
    for i in range(num_children):
        counter.current_id += 1
        children[i] = update_dict_ids(counter, children[i], parent_id=input_dict["id"])
        counter.current_id += len(children[i].get("children", []))
    input_dict["children"] = children

    return input_dict


def convert_structure(vote) -> dict:
    """
    Recursively converts the structure of a budget vote.

    Args:
        vote (dict): A dictionary representing the budget vote in the original structure.

    Returns:
        dict: A dictionary representing the budget vote in the new structure.

    The original structure consists of an array of dictionaries where each dictionary represents a budget vote item.
    Each dictionary has the following keys:
        - "id": the id of the node.
        - "name": the name of the budget vote item.
        - "description": the description of the node (ministry).
        - "parent": the id if the node above the current node.
        - "allocated_budget_amount": the allocated budget amount for the budget vote item.
        - "children": an array of dictionaries representing the children of the budget vote item, if any.

    The new structure consists of a nested dictionary where each dictionary represents a budget vote item.
    Each dictionary has the following keys:
        - "total": the total allocated budget amount for the budget vote item and its children.
        - any child budget vote items as nested dictionaries.
    """

    def _convert_recursive(vote) -> dict:
        result = {}
        # iterate over the children of the current vote item
        for item in vote["children"]:
            # extract the name, children, and total allocated budget amount for the current item
            name = item["name"]
            children = item["children"]
            total = item["allocated_budget_amount"]
            # if the current item has no children, add it to the result with its allocated budget amount
            if len(children) == 0:
                result[name] = total
            # if the current item has children, recursively call this function on its children and add the result to the current item
            else:
                child_result = _convert_recursive({"children": children})
                child_result["total"] = total
                result[name] = child_result
        return result

    # the total allocated budget amount
    total = 0
    # convert the dict
    updated_vote = _convert_recursive(vote)
    # iterate over the values in the updated budget vote and add up the total allocated budget amount in the first level
    for value in updated_vote.values():
        total += float(value["total"])
    # add the total allocated budget amount to the top level of the updated dictionary
    updated_vote["total"] = total

    return updated_vote


def unite_votes(votes: list[dict]) -> dict:
    """
    Convert a list of votes into a dictionary of updated votes with user IDs.

    Args:
        votes: A list of votes, where each vote is represented by a dictionary.

    Returns:
        A dictionary of updated votes, where each vote is represented by a dictionary
        with a user ID as the key.
    """
    # an empty dictionary to store the updated votes
    voted_dict = {}

    # iterate over the list of votes
    for i, vote in enumerate(votes, start=1):
        # convert the vote to the new Simpliler structure
        updated_vote = convert_structure(vote)
        # create a user ID for the current vote
        userId = "user" + str(i)
        # add the updated vote to the dictionary with the user ID as the key
        voted_dict[userId] = updated_vote

    return voted_dict


# =============================================Utility-Functions============================================================
def _run_algorithm(votes: dict, algorithm_number: int) -> dict:
    """
    Runs a specific algorithm on the given votes and returns the result.

    Args:
        votes (dict): A nested dictionary representing the votes of all citizens for the budget.
        algorithm_number (int): The number representing the algorithm to run.
            1 for median_algorithm or 2 for generalized_median_algorithm.

    Raises:
        Exception: If the algorithm_number is not valid.

    Returns:
        dict: A dictionary representing the final result of the algorithm.
    """

    # edge case: empty dictionary (no votes)
    if not bool(votes):
        # print("The dictionary is empty")
        return votes

    num_of_users = len(votes)
    total_budget = votes["user1"]["total"]

    # convert the given dictionary to a tree
    tree = Tree.from_dict(votes)

    # find the values of the leaves for each user and store them in a dictionary
    leaves_values = {}  # {user_number: list_of_its_values}
    for i in range(0, num_of_users):
        root = tree._root
        node = root._children[i]
        leaves = _find_leaves(node)
        leaves_values[i] = leaves

    # choose the algorithm to run based on the input
    if algorithm_number == 1:  # median_algorithm
        median_values = _calculate_median(leaves_values, total_budget, 1)
    elif algorithm_number == 2:  # generalized_median_algorithm
        median_values = _calculate_median(leaves_values, total_budget, 2)
    else:  # wrong input
        raise Exception("Invalid algorithm id!")

    # create the final result dictionary
    result = _create_result(votes, median_values)

    # return the final result dictionary
    return result


def _find_leaves(node) -> list:
    """ "Returns all the leaves of the given node"""
    if not node._children:
        return [node._allocated_budget_amount]
    leaves = []
    for child in node._children:
        # ignore leaves named 'total'
        if child._name != "total":
            leaves += _find_leaves(child)

    return leaves


def _calculate_median(
    votes_by_user: dict, total_budget: float, algorithm_number: int
) -> dict:
    """
    A utility function that calculates the median value of each
    leaf node (project) in a dictionary of budget votes.

    Args:
        votes_by_user (dict): A dictionary where each key represents a user and the value is a list of budget votes
            (floats) for each leaf node (project).
        total_budget (float): The total budget.
        algorithm_number (int): The number representing the algorithm to run.
            1 for median_algorithm or 2 for generalized_median_algorithm.

    Returns:
        dict: A dictionary where each key represents a leaf node (project) and the value is its median budget
            value across all users.
    """

    votes_by_project = {}  # {leaf_number (project): its_values (budget)}
    median_values = {}  # {leaf_number (project): its_median_value}
    # the constants values (will be only used for the 2nd algorithm)
    constants = []

    # add each value of project (leave) to the dictionary
    for user in votes_by_user.keys():
        for count, value in enumerate(list(votes_by_user.values())[user]):
            if count not in votes_by_project:
                votes_by_project[count] = []
            votes_by_project[count].append(value)

    # choose the algorithm to run based on the input
    if algorithm_number == 2:  # generalized_median_algorithm
        num_of_projects = len(votes_by_project)
        constants = _find_median_with_constant_functions(
            votes_by_project=votes_by_project, c=total_budget, n=num_of_projects
        )

    for key, values in votes_by_project.items():
        if key not in median_values:
            median_values[key] = []
        # sort the list of values
        median = statistics.median(values + constants)
        median_values[key] = median

    return median_values


def _find_median(lst: list[float]) -> float:
    """
    A utility function that returns the median value.

    Args:
        lst (List of floats): a list of floats.

    Returns:
        The median number.
    """

    median = 0
    lst_length = len(lst)
    median_index = lst_length // 2
    if lst_length % 2 != 0:
        median = lst[median_index]
    else:
        first_median = lst[median_index - 1]
        second_median = lst[median_index]
        median = (first_median + second_median) / 2

    return median


def _find_median_with_constant_functions(
    votes_by_project: dict,
    c: float,
    n: int,
    min_search: float = 0,
    max_search: float = 1,
    max_iterations: int = 100,
) -> list[float]:
    """
    Find the median of a list of values by adding constant functions.

    Args:
        votes_by_project (dict): A dictionary where each key represents a project and the value is a list of budget votes
            for that project by all the users.
        c (float): The total budget.
        n (int): The number of leaves (projects).
        min_search (float, optional): The minimum value of the search range. Defaults to 0.
        max_search (float, optional): The maximum value of the search range. Defaults to 1.
        max_iterations (int, optional): The maximum number of iterations. Defaults to 100.

    Returns:
        constants list[float]: A list of all the constants values, or None if the maximum number of iterations is reached.
    """
    # calculate the midpoint of the search range
    t = (min_search + max_search) / 2

    constants = _compute_constants(votes_by_project, c, n, t)

    sum_medians = 0
    # use a generator expression to avoid creating a list of all items in memory at once
    for _project, values in (item for item in votes_by_project.items()):
        values_with_constants = _combine_lists(values, constants)
        # find the median
        median = statistics.median(values_with_constants)
        sum_medians += median

    # print('max_iterations: ', max_iterations)
    # print('sum_medians: ', sum_medians)

    EPSILON = 0.0001  # a threshold value
    # base case: if the diff of the sum is small enough
    # or the maximum number of iterations is reached,
    # return the current constants
    if (
        abs(sum_medians - c) < EPSILON * c
        # or max_search - min_search < EPSILON
        or max_iterations <= 0
    ):
        return constants
    # if the sum of the medians is greater than or equal to the total budget, search the lower half of the range
    elif sum_medians >= c:
        return _find_median_with_constant_functions(
            votes_by_project=votes_by_project,
            c=c,
            n=n,
            min_search=min_search,
            max_search=t,
            max_iterations=max_iterations - 1,
        )
    # if the sum of the medians is less than the total budget, search the upper half of the range
    elif sum_medians < c:
        return _find_median_with_constant_functions(
            votes_by_project=votes_by_project,
            c=c,
            n=n,
            min_search=t,
            max_search=max_search,
            max_iterations=max_iterations - 1,
        )


def _compute_median(values_with_constants):
    """Helper function to compute the median of a list of values with constants."""
    return statistics.median(values_with_constants)


def _find_median_with_constant_functions_multithreaded(
    votes_by_project: dict,
    c: float,
    n: int,
    min_search: float = 0,
    max_search: float = 1,
    max_iterations: int = 50,
    num_threads: int = None,
) -> list[float]:
    """
    Find the median of a list of values by adding constant functions using multithreading.

    Args:
        votes_by_project (dict): A dictionary where each key represents a project and the value is a list of budget votes
            for that project by all the users.
        c (float): The total budget.
        n (int): The number of leaves (projects).
        min_search (float, optional): The minimum value of the search range. Defaults to 0.
        max_search (float, optional): The maximum value of the search range. Defaults to 1.
        max_iterations (int, optional): The maximum number of iterations. Defaults to 50.
        num_threads (int, optional): The number of threads to use for parallelization. Defaults to None (use all available cores).

    Returns:
        constants list[float]: A list of all the constants values, or None if the maximum number of iterations is reached.
    """

    # calculate the midpoint of the search range
    t = (min_search + max_search) / 2

    constants = _compute_constants(votes_by_project, c, n, t)

    sum_medians = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # use a generator expression to avoid creating a list of all items in memory at once
        futures = [
            executor.submit(_compute_median, _combine_lists(values, constants))
            for values in votes_by_project.values()
        ]
        # iterate over the completed futures to retrieve the medians and accumulate their sum
        for future in concurrent.futures.as_completed(futures):
            sum_medians += future.result()

    EPSILON = 0.0001  # a threshold value
    # base case: if the diff of the sum is small enough
    # or the maximum number of iterations is reached,
    # return the current constants
    if abs(sum_medians - c) < EPSILON * c or max_iterations <= 0:
        return constants
    # if the sum of the medians is greater than or equal to the total budget, search the lower half of the range
    elif sum_medians >= c:
        return _find_median_with_constant_functions_multithreaded(
            votes_by_project=votes_by_project,
            c=c,
            n=n,
            min_search=min_search,
            max_search=t,
            max_iterations=max_iterations - 1,
            num_threads=num_threads,
        )
    # if the sum of the medians is less than the total budget, search the upper half of the range
    elif sum_medians < c:
        return _find_median_with_constant_functions_multithreaded(
            votes_by_project=votes_by_project,
            c=c,
            n=n,
            min_search=t,
            max_search=max_search,
            max_iterations=max_iterations - 1,
            num_threads=num_threads,
        )


def _combine_lists(list1, list2) -> list:
    """
    Combine two lists into a new list.
    """
    result = list1.copy()
    result.extend(list2)
    return result


def _compute_constants(
    votes_by_project: dict, c: float, n: int, t: float
) -> list[float]:
    """
    Compute the constants for the `_find_median_with_constant_functions` function,
    according to the formula: f_i = c * min{1, i * t}.

    Args:
        votes_by_project (dict): A dictionary where each key represents a project and the value is a list of budget votes
            for that project by all the users.
        c (float): The total budget.
        n (int): The number of leaves (projects).
        t (float): The midpoint of the search range.

    Returns:
        list[float]: A list of `n-1` constants computed using the formula `f_i = c * min(1, i * t)`, rounded to 3 decimal places.
    """
    # create a 1D numpy array containing the values 1 to n-1
    i_arr = np.arange(1, n, dtype=float)
    # compute the constants using the vectorized expression: c * np.minimum(1, i_arr * t)
    constants = np.round(c * np.minimum(1, i_arr * t), 3)
    # convert the numpy array to a Python list and return it
    return constants.tolist()


def _create_result(votes: dict, new_values: list[float]) -> dict:
    """
    A utility funfction that create a dictionary that aggregates user votes with the provided budget values.

    Args:
    - votes (dict): A dictionary representing the votes of each user, where the keys are the users' IDs and the values
      are dictionaries representing their votes.
    - new_values (list[float]): A list of budget values that corresponds to each vote category.

    Returns:
    - A dictionary representing the result of aggregating the user votes with the budget values, with keys
      corresponding to the categories of the votes and nested dictionaries representing subcategories, and values
      representing the budget allocated to each category or subcategory. The "total" key is added to each nested
      dictionary to represent the total budget allocated to the corresponding category or subcategory.
    """

    # the key of the first user in the given dict
    first_key = next(iter(votes))
    # extracts the vote of the first user
    first_user_vote = votes[first_key]
    # create an empty dictionary to hold the final result
    result = {}
    # point the current index in the new_values
    index = {}
    index[0] = 0

    result = _building_nested_dict(first_user_vote, new_values, index, result)
    _calculate_total(result)

    return result


def _building_nested_dict(
    votes: dict, new_values: list, index: list[float], result: dict
) -> dict:
    """
    A utility function that recursively build a new nested dictionary based on
    an input dictionary and a list that contains the updated values.

    Args:
        votes (dict): The input dictionary to build from.
        new_values (list): A list of values to assign to the keys in the input dictionary.
        index (list): A list holding a single integer, representing the current index in the list of values.
        result (dict): A dictionary to add the newly created nested dictionary to.

    Returns:
        dict: A new nested dictionary built from the input dictionary and list of values.
    """

    # create a new dictionary to hold the nested values
    nested_result = {}

    # iterate over the items in the input dictionary
    for key, value in votes.items():
        # if the current value is a nested dictionary, recursively call the function
        if isinstance(value, dict):
            nested_result[key] = _building_nested_dict(value, new_values, index, result)
        else:
            # if the current key is "total", leave empty
            if key == "total":
                nested_result[key] = ""
            else:
                nested_result[key] = new_values[index[0]]
                index[0] += 1

    return nested_result


def _calculate_total(budget: dict) -> float:
    """
    A utility function that recursively calculates the total budget
    for each level of a nested dictionary and assigns it to the 'total' key.
    The function updates the total keys in the given budget.

    Args:
        budget (dict): A nested dictionary representing a budget.

    Returns:
        float: The total budget at the highest level of the dictionary.
    """

    total = 0
    for key, value in budget.items():
        if isinstance(value, dict):
            # if the value is a dictionary, recursively calculate its total budget and assign it to the 'total' key
            sub_dept_budget = _calculate_total(value)
            budget[key]["total"] = sub_dept_budget
            total += sub_dept_budget
        elif isinstance(value, (int, float)):
            # if the value is an integer or a float, add it to the total budget
            total += value
    # assign the total budget to the 'total' key of the current level
    budget["total"] = total

    return total
