import copy

from src.algorithm.utils import filter_bids, find_max
import logging
logger = logging.getLogger("equal_shares_logger")

CONTINUOUS_COST = 1  # A cost that signals that the given project is in its continuous increment phase.
DISTRIBUTION_PARAMETER_COST = 10000 # A const showing the budget distribution parameter#


def equal_shares(
    voters: list[int],
    projects_costs: dict[int, int],  # min cost per project
    budget: int,
    bids: dict[int, dict[int, int]],
) -> tuple[dict[int, int], dict[int, dict[int, float]]]:
    '''

        :argument
            voters (list): A list of voter names.
            projects_costs (list): A dictionary mapping project IDs to their min cost.
            budget (int): The total budget available for all the projects.
            bids (dict): A dictionary mapping project IDs to the
            list of voters who approve them and the cost the voters chose.

        :return
            tuple[dict[int, int], dict[int, dict[int, float]]]:
            first: A dictionary of the mapping the received project IDs for the maximum cost given for them
            second: A dictionary that maps the IDs of the projects received for the cost each voter gave them

    '''

    projects = projects_costs.keys()
    max_bid_for_project = find_max(bids)
    rounded_budget = int(budget / len(voters)) * len(voters)  # start with integral per-voter voters_budget
    logger.info("\nRunning equal_shares: budget=%s, rounded to %s", budget, rounded_budget)

    winners_allocations, projects_costs_of_next_increase, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, rounded_budget, bids, max_bid_for_project
    )
    total_chosen_project_cost = sum(winners_allocations[c] for c in winners_allocations)
    logger.info("total_chosen_project_cost=%s", total_chosen_project_cost)


    while True:
        # Check if current outcome is exhaustive
        is_exhaustive = True
        for candidate in projects:
            candidate_cost_of_next_increase = projects_costs_of_next_increase[candidate]
            # check if total cost of chosen project + current project  <= budget, if true have more project to chack
            # check if total cost of chosen project + project_cost   <= budget
            # and total project_cost + curr project_cost <= max value for curr project,
            if (
                (total_chosen_project_cost + candidate_cost_of_next_increase <= budget)
                and (winners_allocations[candidate] + candidate_cost_of_next_increase <= max_bid_for_project[candidate])
                and (candidate_cost_of_next_increase > 0)

            ):
                is_exhaustive = False
                logger.debug("Candidate %s is not fully funded - allocation is not exhaustive", candidate)
                break
        if is_exhaustive:
            break

        # would the next highest voters_budget work?
        updated_rounded_budget = rounded_budget + len(voters)*(budget/DISTRIBUTION_PARAMETER_COST)  # Add DISTRIBUTION_PARAMETER_COST to each voter's voters_budget

        updated_winners_allocations, projects_costs_of_next_increase, updated_candidates_payments_per_voter = (
            equal_shares_fixed_budget(
                voters,
                projects_costs,
                updated_rounded_budget,
                bids,
                max_bid_for_project,
            )
        )
        total_chosen_project_cost = sum(updated_winners_allocations[c] for c in updated_winners_allocations)
        logger.info("total_chosen_project_cost=%s", total_chosen_project_cost)

        if total_chosen_project_cost > budget:
            logger.info("total_chosen_project_cost is more than the budget %s; breaking", budget)
            break

        # Else, keep increasing the budget
        rounded_budget = updated_rounded_budget
        winners_allocations = updated_winners_allocations
        candidates_payments_per_voter = updated_candidates_payments_per_voter

    return winners_allocations, candidates_payments_per_voter





def break_ties(cost: dict[int, int], bids: dict[int, dict[int, int]], candidates: list[int]) -> list[int]:
    """
    break ties
    first the min cost project
    second the max voter for project
    Ensure there is only one remaining project, third the min index project
    """

    remaining = candidates
    best_cost = min(cost[c] for c in remaining)  # first the min cost project
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(bids[c]) for c in remaining)  # second the max voter for project
    remaining = [c for c in remaining if len(bids[c]) == best_count]
    remaining = [min(remaining)]  # Ensure there is only one remaining project, third the min index project
    return remaining


def equal_shares_fixed_budget(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: int,
    bids: dict[int, dict[int, int]],
    max_bid_for_project: dict,
) -> tuple[dict[int, int], dict[int, int], dict[int, dict[int, float]]]:
    logger.info("\nRunning equal_shares_fixed_budget: budget=%s", budget)
    projects = projects_costs.keys()

    voters_budgets = {i: budget / len(voters) for i in voters}
    # logger.debug("Initial voters_budgets: %s", voters_budgets)

    candidates_payments_per_voter = {
        candidate: {voter: 0.0 for voter in inner_dict.keys()} for candidate, inner_dict in bids.items()
    }
    # logger.debug("Initial candidates_payments_per_voter:\n   %s", candidates_payments_per_voter)

    remaining_candidates = {
        candidate: len(bids[candidate])
        for candidate in projects
        if projects_costs[candidate] > 0 and len(bids[candidate]) > 0
    }  # remaining candidate -> previous effective vote count
    winners_allocations = {
        candidate: 0 for candidate in projects
    }  # Initialize amount invested in each winning projects

    updated_bids = copy.deepcopy(bids)
    updated_cost = copy.deepcopy(projects_costs)


    while True:
        best_candidates = []
        best_effective_vote_count = 0.0 # best = the max effective supporters in all projects

        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_candidates_sorted = {
            candidate: effective_vote_count
            for candidate, effective_vote_count in sorted(
                remaining_candidates.items(), key=lambda item: item[1], reverse=True
            )
        }

        logger.debug(
            "\nRemaining candidates sorted by decreasing previous effective vote count:\n   %s",
            remaining_candidates_sorted,
        )
        logger.debug("Voters' budgets:\n   %s", voters_budgets)

        for candidate, previous_effective_vote_count in remaining_candidates_sorted.items():
            if previous_effective_vote_count < best_effective_vote_count:
                logger.debug(
                    "Candidate %s: Previous effective vote count (%s) < best_effective_vote_count (%s): breaking",
                    candidate,
                    previous_effective_vote_count,
                    best_effective_vote_count,
                )
                break
            money_behind_candidate = sum(
                voters_budgets[i] for i in updated_bids[candidate].keys() if updated_bids[candidate][i] > 0
            )
            if money_behind_candidate < updated_cost[candidate]:
                # candidate is not affordable - The total amount of money is less than the candidate cost
                logger.debug(
                    "Candidate %s not affordable: supporters have %s but updated_cost = %s",
                    candidate,
                    money_behind_candidate,
                    updated_cost[candidate],
                )
                del remaining_candidates[candidate]
                    # The candidate cannot be purchased, so remove him from the candidate list
                continue

            # Calculate the effective vote count of candidate:
            sorted_approvers = {
                voter: voters_budgets[voter]
                for voter in sorted(updated_bids[candidate].keys(), key=lambda i: voters_budgets[i])
            }

            denominator = len(sorted_approvers)
            paid_so_far = 0.0
            for i, budget_of_i in sorted_approvers.items():
                # compute payment if remaining approvers pay equally
                equal_payment = (updated_cost[candidate] - paid_so_far) / denominator
                if budget_of_i < equal_payment:
                    # i cannot afford the payment, so pays entire remaining budget_of_i
                    paid_so_far += budget_of_i
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    effective_vote_count = updated_cost[candidate] / equal_payment
                    if effective_vote_count > best_effective_vote_count:
                        best_effective_vote_count = effective_vote_count
                        best_candidates = [candidate]
                    elif effective_vote_count == best_effective_vote_count:
                        best_candidates.append(candidate)
                    break
            logger.debug(
                "Candidate %s: cost %s; approvers and budgets=%s; effective_vote_count=%s",
                candidate,
                updated_cost[candidate],
                sorted_approvers,
                effective_vote_count,
            )
        logger.debug("best_candidates: %s", best_candidates)
        if not best_candidates:
            logger.debug("No remaining candidates are affordable.")
            break  # Break out of the outer "while True" loop

        best_found = break_ties(updated_cost, updated_bids, best_candidates)
        logger.debug("best_found after tie-breaking: %s", best_found)

        if len(best_found) > 1:
            raise Exception(
                f"Tie-breaking failed: tie between projects {best_found} "
                + "could not be resolved. Another tie-breaking needs to be added."
            )
        chosen_candidate = best_found[0]

        """
        After receiving the selected project, we reduce the cost of the selected project from the Update_bids list
        and create a new project with a "factor" cost, we filter its data using the
        filter_bids function.Then they check whether the total price of the project
        does not exceed the highest price they chose.
        and update "remaining" with the number of voters who chose it at the new price. and continue the while loop.
        """

        chosen_candidate_max_bid = max_bid_for_project[chosen_candidate]
        chosen_candidate_cost = updated_cost[chosen_candidate]
        chosen_candidate_bids = updated_bids[chosen_candidate]
        logger.debug(
            "Chosen project: %s, current cost: %s, max bid: %s, updated bids: %s",
            chosen_candidate,
            chosen_candidate_cost,
            chosen_candidate_max_bid,
            chosen_candidate_bids,
        )


        if chosen_candidate_cost == CONTINUOUS_COST:
            positive_bids = {
                voter: bid for voter, bid in chosen_candidate_bids.items() if bid > 0 and voters_budgets[voter] > 0

            }
            """
            The chosen project is in its continuous phase. We increase its allocation up to one of the following thresholds:
            1. The allocation attains the maximum possible cost for the project:  chosen_candidate_max_bid
            2. The addition attains the smallest bid of a supporter: min(bid for voter, bid in positive_bids.items())
            3. The addition attains the sum of budgets of all supporters.
            """
            chosen_candidate_cost = min(
                chosen_candidate_max_bid - winners_allocations[chosen_candidate],
                min(bid for voter, bid in positive_bids.items()),
                sum(voters_budgets[voter] for voter, bid in positive_bids.items()),
            )
            logger.debug(
                "   Chosen project is now in the continuous phase - changing the cost to %s", chosen_candidate_cost
            )

        # Deducts from the voters_budget of each voter who chose the current
        # project the relative part for the current project
        #
        best_max_payment = chosen_candidate_cost / best_effective_vote_count
        for i in chosen_candidate_bids.keys():
            if voters_budgets[i] > best_max_payment:
                voter_payment = best_max_payment
                logger.debug("   Voter %s pays his relative part %s", i, voter_payment)
            else:
                voter_payment = voters_budgets[i]
                logger.debug("   Voter %s pays his entire remaining budget %s", i, voter_payment)
            voters_budgets[i] -= voter_payment
            candidates_payments_per_voter[chosen_candidate][i] += voter_payment
        winners_allocations[chosen_candidate] += chosen_candidate_cost

        # check if the curr cost + total update codt <= max value for this projec
        # logger.info(" total project price   = %s", winners_total_cost[chosen_candidate])

        if winners_allocations[chosen_candidate] < chosen_candidate_max_bid:
            filter_bids(
                updated_bids,
                chosen_candidate,
                chosen_candidate_cost,
                CONTINUOUS_COST,
                updated_cost,
            )
            # Updates the remaining list in the number of voters after updating the price of the project
            remaining_candidates[chosen_candidate] = len(updated_bids[chosen_candidate].keys())
            logger.debug(
                (
                    "Candidate %s now has allocation %s. Going to continuous phase:"
                    " setting new cost to %s, new effective vote count = %s"
                ),
                chosen_candidate,
                winners_allocations[chosen_candidate],
                updated_cost[chosen_candidate],
                remaining_candidates[chosen_candidate],
            )
        else:
            updated_cost[chosen_candidate] = 0
            del remaining_candidates[chosen_candidate]
            logger.debug(
                "Candidate %s now has the maximum possible allocation: %s. Setting new cost to %s",
                chosen_candidate,
                winners_allocations[chosen_candidate],
                updated_cost[chosen_candidate],
            )
    logger.info("winners_allocations: %s", winners_allocations)
    logger.info("Cost for next increase: %s", updated_cost)
    return winners_allocations, updated_cost, candidates_payments_per_voter
