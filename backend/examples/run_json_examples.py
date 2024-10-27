import json
import logging
from src.algorithm.public import PublicEqualSharesInput
from src.logger import LoggerName, get_logger

from src.algorithm.computation import min_max_equal_shares
from src.algorithm.average_first import average_first
from src.algorithm.utils import calculate_average_bids, get_project_min_costs, get_project_max_costs


def get_bid_sums(voters: list, bids: dict) -> dict:
    bid_sums = {}
    for voter in voters:
        voter_total_bid = 0
        for project, project_bids in bids.items():
            if voter in project_bids:
                voter_total_bid += project_bids[voter]
        bid_sums[voter] = voter_total_bid
    return bid_sums


def normalize_bids(voters: list, bids: dict, bid_sums: dict, budget: int) -> dict:
    normalized_project_bids = dict()
    for project, project_bids in bids.items():
        normalized_project_bids[project] = {
            voter: int(bid * budget / bid_sums[voter]) for voter, bid in project_bids.items()
        }
    return normalized_project_bids


def run_json_example(input_json_path: str, results_json_path: str = "") -> None:
    with open(input_json_path, "r") as f:
        data_json = json.load(f)
    # print(data)
    data = PublicEqualSharesInput(**data_json)

    bid_sums = get_bid_sums(data.voters, data.bids)
    print("bid sums: ", bid_sums, "\n")

    normalized_bids = normalize_bids(data.voters, data.bids, bid_sums, data.budget)
    normalized_bid_sums = get_bid_sums(data.voters, normalized_bids)
    print("normalized bid sums: ", normalized_bid_sums, "\n")

    # normalized_bids = data.bids

    project_min_costs = get_project_min_costs(data.cost_min_max)
    project_max_costs = get_project_max_costs(data.cost_min_max)

    averages = calculate_average_bids(normalized_bids, data.voters)
    total_allocation = sum([allocation for project, allocation in averages.items()])
    print(f"\naverages: \nwinners_allocations={averages}\ntotal_allocation={total_allocation}")

    mes_winners, candidates_payments_per_voter = min_max_equal_shares(
        data.voters, data.cost_min_max, data.budget, normalized_bids, use_plt=False
    )
    total_allocation = sum([allocation for project, allocation in mes_winners.items()])
    print(f"\nmin_max_equal_shares: \nwinners_allocations={mes_winners}\ntotal_allocation={total_allocation}")

    averagefirst_winners, candidates_payments_per_voter = average_first(
        data.voters, data.cost_min_max, data.budget, normalized_bids, use_plt=False
    )
    total_allocation = sum([allocation for project, allocation in averagefirst_winners.items()])
    print(f"\naverage_first: \nwinners_allocations={averagefirst_winners}\ntotal_allocation={total_allocation}")

    print("Project,Minimum,Average,AverageThenMES,MES,Maximum")
    for project, avg in averages.items():
        min_cost = project_min_costs[project]
        max_cost = project_max_costs[project]
        average = averages[project]
        mes_win = mes_winners[project]
        avgmes_win = averagefirst_winners[project]
        print(f"{project},{min_cost},{average},{avgmes_win},{mes_win},{max_cost}")

    # res = public_equal_shares(data)
    # if results_json_path:
    #     with open(results_json_path, "w") as f:
    #         json.dump(res.model_dump()["results"], f, indent=2)


if __name__ == "__main__":
    get_logger(LoggerName.ALGORITHM).setLevel(logging.INFO)
    get_logger(LoggerName.ALGORITHM).addHandler(logging.StreamHandler())

    run_json_example("experiment_with_10_council_members.json", "experiment_with_10_council_members_results.json")
    # run_json_example("experiment_with_200_students.json", "experiment_with_200_students_results.json")
