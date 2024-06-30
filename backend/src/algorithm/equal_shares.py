import copy
import logging

# from src.algorithm.utils import filter_bids, find_max
from utils import filter_bids, find_max

logger = logging.getLogger("equal_shares_logger")


def equal_shares(
    voters: list[int],
    projects: list[int],
    cost: dict[int, int],              # min cost per project
    approvers: dict[int, int],
    budget: int,
    bids: dict[int, dict[int, int]],
    budget_increment_per_project: int,
) -> tuple[list[int], dict[int, int], dict[int, dict[int, float]]]:
    """
    # T.0
    >>> voters = [1, 2, 3, 4, 5]  # Voters
    >>> projects = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]  # Project IDs
    >>> cost = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    >>> approvers = {
    ...     11: [1, 2, 4],
    ...     12: [2, 5],
    ...     13: [1, 5],
    ...     14: [3, 4],
    ...     15: [2, 3, 5],
    ...     16: [2, 5],
    ...     17: [1, 4],
    ...     18: [2, 5],
    ...     19: [1, 3, 5],
    ...     20: [2, 3]
    ... }
    >>> bids = {
    ...     11: {1: 100, 2: 100, 4: 100},
    ...     12: {2: 150, 5: 150},
    ...     13: {1: 200, 5: 200},
    ...     14: {3: 250, 4: 250, },
    ...     15: {2: 300, 3: 300, 5: 300},
    ...     16: {2: 350, 5: 350},
    ...     17: {1: 400, 4: 400},
    ...     18: {2: 450, 5: 450},
    ...     19: {1: 500, 3: 500,5: 500},
    ...     20:{2: 550, 3: 550}
    ... }
    >>> budget = 900  # Total budget
    >>> budget_increment_per_project = 10
    >>> equal_shares(
    ...     voters,
    ...     projects,
    ...     cost,
    ...     approvers,
    ...     budget,
    ...     bids,
    ...     budget_increment_per_project
    ... )
    ([11, 13, 14, 15], {11: 100, 12: 0, 13: 200, 14: 250, 15: 300, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}, {11: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336}, 12: {2: 0, 5: 0}, 13: {1: 108.0, 5: 0}, 14: {3: 0, 4: 158.0}, 15: {2: 100.0, 3: 100.0, 5: 100.0}, 16: {2: 0, 5: 0}, 17: {1: 0, 4: 0}, 18: {2: 0, 5: 0}, 19: {1: 0, 3: 0, 5: 0}, 20: {2: 0, 3: 0}})
    """

    max_cost_for_project = find_max(bids)
    chosen_project, chosen_project_cost, update_cost, budget_per_voter = equal_shares_fixed_budget(
        voters, projects, cost, approvers, budget, bids, budget_increment_per_project, max_cost_for_project
    )

    # add 1 completion
    # start with integral per-voter voters_budget
    voters_budget = int(budget / len(voters)) * len(voters)
    total_chosen_project_cost = sum(chosen_project_cost[c] for c in chosen_project_cost)

    while True:
        # is current outcome exhaustive?
        is_exhaustive = True
        for project in projects:
            max_value_project = max_cost_for_project[project]
            project_cost = update_cost[project]

            # check if total cost of chosen project + current project  <= budget, if true have more project to chack
            # check if total cost of chosen project + project_cost   <= budget
            # and total project_cost + curr project_cost <= max value for curr project,
            # if true thr price of the project can be increased

            if (project not in chosen_project and total_chosen_project_cost + cost[project] <= budget) or (
                project in chosen_project
                and total_chosen_project_cost + project_cost <= budget
                and chosen_project_cost[project] + project_cost <= max_value_project
            ):
                is_exhaustive = False

                break
        # if so, stop
        if is_exhaustive:
            break
        # would the next highest voters_budget work?
        update_voters_budget = voters_budget + len(voters)  # Add 1 to each voter's voters_budget
        logger.info(
            "  Call fix voters_budget   = %s B= %s, %s", total_chosen_project_cost, budget, update_voters_budget
        )
        update_chosen_project, update_chosen_project_cost, update_cost, update_budget_per_voter = (
            equal_shares_fixed_budget(
                voters,
                projects,
                cost,
                approvers,
                update_voters_budget,
                bids,
                budget_increment_per_project,
                max_cost_for_project,
            )
        )
        total_chosen_project_cost = sum(update_chosen_project_cost[c] for c in update_chosen_project_cost)

        if total_chosen_project_cost <= budget:
            # yes, so continue with that voters_budget
            voters_budget = update_voters_budget
            chosen_project = update_chosen_project
            chosen_project_cost = update_chosen_project_cost
            budget_per_voter = update_budget_per_voter
        else:
            # logger.info("  break total_chosen_project_cost  = %s B= %s", total_chosen_project_cost, B)
            # no, so stop
            break

    return chosen_project, chosen_project_cost, budget_per_voter


"""
break ties
first the min cost project
second the max voter for project
Ensure there is only one remaining project, third the min index project
"""


def break_ties(
    cost: dict[int, int], approvers: dict[int, dict[int, int]], bids: list[int, dict[int, int]]
) -> list[int]:
    remaining = bids.copy()
    best_cost = min(cost[c] for c in remaining)  # first the min cost project
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(approvers[c]) for c in remaining)  # second the max voter for project
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    remaining = [min(remaining)]  # Ensure there is only one remaining project, third the min index project
    return remaining


def equal_shares_fixed_budget(
    voters: list[int],
    projects: list[int],
    cost: dict[int, int],
    approvers: dict[int],
    budget: int,
    bids: dict[int, dict[int, int]],
    budget_increment_per_project: int,
    max_cost_for_project: dict,
) -> tuple[list[int], dict[int, int], dict[int, int], dict[int, dict[int, int]]]:
    logger.info("\nRunning equal_shares_fixed_budget: budget=%s, bids=%s", budget,bids)

    voters_budgets = {i: budget / len(voters) for i in voters}
    logger.debug("Initial voters_budgets=%s", voters_budgets)

    budget_per_voter = {candidate: {voter: 0 for voter in inner_dict.keys()} for candidate, inner_dict in bids.items()}
    logger.debug("Initial budget_per_voter=%s", budget_per_voter)

    remaining = {candidate: len(approvers[candidate]) for candidate in projects if cost[candidate] > 0 and len(approvers[candidate]) > 0}  # remaining candidate -> previous effective vote count
    logger.debug("remaining=%s", remaining)

    winners = []  # Initialize list of winning projects
    winners_allocation = {candidate: 0 for candidate in projects}  # Initialize amount invested in each winning projects

    updated_bids = copy.deepcopy(bids)
    updated_approvers = copy.deepcopy(approvers)
    updated_cost = copy.deepcopy(cost)

    while True:
        best_candidates = []
        best_effective_vote_count = 0

        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_candidates_sorted = sorted(remaining.keys(), key=lambda candidate: remaining[candidate], reverse=True)
        logger.debug("Remaining candidates sorted by decreasing effective vote count: x%s", remaining_candidates_sorted)

        for candidate in remaining_candidates_sorted:
            previous_eff_vote_count = remaining[candidate]
            if previous_eff_vote_count < best_effective_vote_count:
                # c cannot be better than the best so far
                # logger.info("c cannot be better than the best so far c=%s", c)

                break
            money_behind_now = sum(voters_budgets[i] for i in updated_approvers[candidate])
            if money_behind_now < updated_cost[candidate]:
                # c is not affordable
                del remaining[candidate]
                # logger.info("c is not affordable c=%s, update_cost for c=%s ", update_cost[c])
                continue
            # calculate the effective vote count of c
            updated_approvers[candidate].sort(key=lambda i: voters_budgets[i])
            paid_so_far = 0
            denominator = len(updated_approvers[candidate])
            for i in updated_approvers[candidate]:
                # compute payment if remaining approvers pay equally
                max_payment = (updated_cost[candidate] - paid_so_far) / denominator
                eff_vote_count = updated_cost[candidate] / max_payment
                if max_payment > voters_budgets[i]:
                    # i cannot afford the payment, so pays entire remaining voters_budget
                    paid_so_far += voters_budgets[i]
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    remaining[candidate] = int(eff_vote_count)
                    if eff_vote_count > best_effective_vote_count:
                        best_effective_vote_count = eff_vote_count
                        best_candidates = [candidate]
                    elif eff_vote_count == best_effective_vote_count:
                        best_candidates.append(candidate)

                    break
        if not best_candidates:
            # logger.info(" no remaining candidates are affordable ,best = %s", best)

            break
        best_found = break_ties(updated_cost, updated_approvers, best_candidates)
        # logger.info(" after vreak ties ,best  = %s", best)

        if len(best_found) > 1:
            raise Exception(
                f"Tie-breaking failed: tie between projects {best_found} "
                + "could not be resolved. Another tie-breaking needs to be added."
            )
        best_candidates = best_found[0]
        winners.append(best_candidates)
        winners = list(set(winners))

        logger.info("  ,winners  = %s", winners)

        """

        After receiving the selected project, we reduce the cost of the selected project from the Update_bids list
        and create a new project with a "factor" cost, we filter its data using the
        filter_bids function.Then they check whether the total price of the project
        does not exceed the highest price they chose.
        and update "remaining" with the number of voters who chose it at the new price. and continue the while loop.

        """

        # the project curr id number and  cost

        curr_project_id = best_candidates
        curr_project_cost = updated_cost[best_candidates]

        logger.info(" id and cost for the chosen project   = %s, %s", curr_project_id, curr_project_cost)

        # Find the highest choice for the current project
        max_value_project = max_cost_for_project[curr_project_id]
        # Deducts from the voters_budget of each voter who chose the current
        # project the relative part for the current project

        best_max_payment = curr_project_cost / best_effective_vote_count

        for i in updated_bids[curr_project_id].keys():
            if voters_budgets[i] > best_max_payment:
                voters_budgets[i] -= best_max_payment
                budget_per_voter[curr_project_id][i] = budget_per_voter[curr_project_id][i] + best_max_payment
            else:
                voters_budgets[i] = 0

        # check if the curr cost + total update codt <= max value for this projec
        # logger.info(" total project price   = %s", winners_total_cost[curr_project_id])

        if winners_allocation[curr_project_id] + curr_project_cost <= max_value_project:

            filter_bids(
                updated_bids,
                updated_approvers,
                curr_project_id,
                curr_project_cost,
                budget_increment_per_project,
                updated_cost,
            )

            winners_allocation[curr_project_id] = winners_allocation[curr_project_id] + curr_project_cost

            # Updates the remaining list in the number of voters after updating the price of the project
            remaining[curr_project_id] = len(updated_bids[curr_project_id].keys())

        else:

            updated_cost[curr_project_id] = 0
            del remaining[curr_project_id]

    # logger.info("winners return  = %s", winners)
    return winners, winners_allocation, updated_cost, budget_per_voter


if __name__=="__main__":
    import doctest
    print("\n",doctest.testmod(),"\n")

    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    voters = [1, 2, 3, 4, 5] 
    projects = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20] 
    cost = {11: 100, 12: 150, 13: 200, 14: 250, 15: 300, 16: 350, 17: 400, 18: 450, 19: 500, 20: 550}
    approvers = {
        11: [1, 2, 4],
        12: [2, 5],
        13: [1, 5],
        14: [3, 4],
        15: [2, 3, 5],
        16: [2, 5],
        17: [1, 4],
        18: [2, 5],
        19: [1, 3, 5],
        20: [2, 3]
    }
    bids = {
        11: {1: 100, 2: 100, 4: 100},
        12: {2: 150, 5: 150},
        13: {1: 200, 5: 200},
        14: {3: 250, 4: 250, },
        15: {2: 300, 3: 300, 5: 300},
        16: {2: 350, 5: 350},
        17: {1: 400, 4: 400},
        18: {2: 450, 5: 450},
        19: {1: 500, 3: 500,5: 500},
        20:{2: 550, 3: 550}
    }
    budget = 900  # Total budget
    budget_increment_per_project = 10
    print(equal_shares_fixed_budget(
        voters,
        projects,
        cost,
        approvers,
        budget,
        bids,
        budget_increment_per_project,
        max_cost_for_project = find_max(bids)
    ))
