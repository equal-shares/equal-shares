import time

from pydantic import BaseModel

from src.algorithm.computation import min_max_equal_shares


class PublicEqualSharesInput(BaseModel):
    voters: list[int]
    cost_min_max: list[dict[int, tuple[int, int]]]
    budget: int
    bids: dict[int, dict[int, int]]


class PublicEqualSharesResponse(BaseModel):
    results: dict[int, int]


def public_equal_shares(data: PublicEqualSharesInput) -> PublicEqualSharesResponse:
    results = _run_equal_shares(data.voters, data.cost_min_max, data.budget, data.bids)
    return PublicEqualSharesResponse(results=results)


def _run_equal_shares(
    voters: list[int], cost_min_max: list[dict[int, tuple[int, int]]], budget: int, bids: dict[int, dict[int, int]]
) -> dict[int, int]:
    start_time = time.time()
    winners_allocations, candidates_payments_per_voter = min_max_equal_shares(voters, cost_min_max, budget, bids)
    end_time = time.time()

    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.0 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)  # Record the end time
    print("----------------------------------------------------------------------------------")
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    print(" T.0 result: ", winners_allocations)
    print(candidates_payments_per_voter)
    print(f"Function executed in {elapsed_time:.4f} seconds")
    # Iterate over each entry in the bids dictionary
    total_sum = 0
    for bid in winners_allocations.values():
        total_sum += bid  # Add the value where the key is 1
    # Output the result
    print("The sum of all Projects:", total_sum, ", budget - total = ", budget - total_sum)  # Record the end time
    print("----------------------------------------------------------------------------------")

    return winners_allocations
