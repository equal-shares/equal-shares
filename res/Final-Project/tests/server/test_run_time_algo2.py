import sys

sys.path.append("../..")
import time

import numpy as np

from src.server.algorithms import (
    _find_median_with_constant_functions,
    _find_median_with_constant_functions_multithreaded,
)

if __name__ == "__main__":
    # each key represents a project and the value is a list of budget votes for that project by all the users.
    votes_by_project = {}
    # The total budget
    c = 100000000
    # The number of leaves (projects)
    n = 5000
    # num of users
    u = 200

    votes_by_user = []
    for user in range(u):
        user_votes = np.random.random(n)
        user_votes = c * user_votes / sum(user_votes)
        votes_by_user.append(user_votes)

    for i in range(n):
        votes_by_project[i] = [vote[i] for vote in votes_by_user]

    print("Singlethread")
    # get the start time
    st = time.time()
    _find_median_with_constant_functions(votes_by_project, c, n)
    # get the end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print("Execution time:", elapsed_time, "seconds")

    print("Multithreaded")
    # get the start time
    st = time.time()
    _find_median_with_constant_functions_multithreaded(votes_by_project, c, n)
    # get the end time
    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print("Execution time:", elapsed_time, "seconds")
