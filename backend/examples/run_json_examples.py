import json
import logging
from src.algorithm.public import PublicEqualSharesInput
from src.algorithm.equal_shares import logger as equal_shares_logger

from src.algorithm.computation import min_max_equal_shares
from src.algorithm.equal_shares import equal_shares_fixed_budget
from src.algorithm.average_first import average_first
from src.algorithm.utils import find_max, remove_invalid_bids, calculate_average_bids, get_project_min_costs, get_project_max_costs, remove_zero_bids, normalize_bids


def get_bid_sums(voters: list, bids: dict) -> dict:
    bid_sums = {}
    for voter in voters:
        voter_total_bid = 0
        for project, project_bids in bids.items():
            if voter in project_bids:
                voter_total_bid += project_bids[voter]
        bid_sums[voter] = voter_total_bid
    return bid_sums



def count_supporters(bids: dict) -> dict:
    map_project_to_supporter_count = {}
    for project, project_bids in bids.items():
        map_project_to_supporter_count[project] = sum(
            1 for voter,bid in project_bids.items() if bid>0
        )
    return map_project_to_supporter_count



def run_json_example(input_json_path: str) -> None:
    """
    Run several algorithms on the input in the given JSON file,
    and print the results to the console.

    Used for development only - for comparing different algorithms.
    """
    with open(input_json_path, "r") as f:
        data_json = json.load(f)
    # print(data)
    data = PublicEqualSharesInput(**data_json)
    data.bids = remove_zero_bids(data.bids)

    bid_sums = get_bid_sums(data.voters, data.bids)
    for voter,bidsum in bid_sums.items():
        if bidsum<290000:
            print(f"voter {voter} has small bid sum {bidsum}.")

    normalized_bids = normalize_bids(data.voters, data.bids, bid_sums, data.budget)
    normalized_bid_sums = get_bid_sums(data.voters, normalized_bids)
    # print("normalized bid sums: ", normalized_bid_sums, "\n")

    normalized_bids = data.bids

    map_project_to_supporter_count = count_supporters(data.bids)
    num_voters = len(data.voters)

    project_min_costs = get_project_min_costs(data.cost_min_max)
    project_max_costs = get_project_max_costs(data.cost_min_max)

    averages = calculate_average_bids(normalized_bids, data.voters)
    total_allocation = sum([allocation for project, allocation in averages.items()])
    print(f"\naverages: \nwinners_allocations={averages}\ntotal_allocation={total_allocation}")

    print("\n\n=== min_max_equal_shares ===\n")
    equal_shares_logger.setLevel(logging.WARNING)
    # mes_winners, candidates_payments_per_voter = min_max_equal_shares(
    #     data.voters, data.cost_min_max, data.budget, normalized_bids, use_plt=False
    # )

    equal_shares_logger.setLevel(logging.INFO)
    equal_shares_logger.addHandler(logging.FileHandler("real-2024-12-05.log", mode="w"))
    bids = remove_invalid_bids(data.voters, data.bids)
    max_bid_for_project = find_max(bids)
    projects_min_costs = get_project_min_costs(data.cost_min_max)
    mes_winners, _, _ = equal_shares_fixed_budget(
        data.voters, projects_min_costs, 3106376, bids, max_bid_for_project
    )

    total_allocation = sum([allocation for project, allocation in mes_winners.items()])
    print(f"\nmin_max_equal_shares: \nwinners_allocations={mes_winners}\ntotal_allocation={total_allocation}")
    equal_shares_logger.setLevel(logging.WARNING)
    return

    print("\n\n=== average_first ===\n")
    equal_shares_logger.setLevel(logging.ERROR)
    averagefirst_winners, candidates_payments_per_voter = average_first(
        data.voters, data.cost_min_max, data.budget, normalized_bids, use_plt=False
    )
    total_allocation = sum([allocation for project, allocation in averagefirst_winners.items()])
    print(f"\naverage_first: \nwinners_allocations={averagefirst_winners}\ntotal_allocation={total_allocation}")
    TAB=","
    print(f"Project{TAB}Minimum{TAB}Average{TAB}Support{TAB}AverageThenMES{TAB}MES{TAB}Maximum")
    for project, avg in averages.items():
        min_cost = project_min_costs[project]
        max_cost = project_max_costs[project]
        average = averages[project]
        support_count = map_project_to_supporter_count[project]
        support_percent = (100*support_count)/num_voters
        support_budget = (data.budget*support_count)/num_voters
        support = f"{support_count} ({support_percent}%, {support_budget} ILS)"
        mes_win = mes_winners[project]
        avgmes_win = averagefirst_winners[project]
        print(f"{project}{TAB}{min_cost}{TAB}{average}{TAB}{support_budget}{TAB}{avgmes_win}{TAB}{mes_win}{TAB}{max_cost}")


def run_json_and_save_output(input_json_path: str, results_json_path:str) -> None:
    """
    Run the algorithm on the input in the given JSON file,
    and print the results to the given JSON path.

    Used for computing actual algorithm results, for uploading to the website API.

    Code adapted from the file src/cli.py .
    """
    from src.algorithm.public import PublicEqualSharesInput, public_equal_shares
    import os

    if not os.path.exists(input_json_path):
        print(f"Error: input-json-path '{input_json_path}' does not exist.")
        return

    # if results_json_path is not None and os.path.exists(results_json_path):
    #     print(f"Error: results-json-path '{results_json_path}' already exists.")
    #     return

    with open(input_json_path, "r") as f:
        data = json.load(f)


    equal_shares_logger.setLevel(logging.WARNING)
    res = public_equal_shares(PublicEqualSharesInput(**data))

    if results_json_path:
        with open(results_json_path, "w") as f:
            json.dump(res.model_dump()["results"], f, indent=2)




if __name__ == "__main__":
    equal_shares_logger.addHandler(logging.StreamHandler())

    # run_json_example("experiment_with_10_council_members.json")
    # run_json_example("experiment_with_200_students.json")
    run_json_example("real-2024-12-05.json")
    # run_json_and_save_output("real-2024-12-05.json", "real-2024-12-05-results.json")
