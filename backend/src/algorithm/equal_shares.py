import copy
import logging
from typing import Any

from src.algorithm.utils import filter_bids, find_max, remove_invalid_bids, remove_zero_bids
from src.logger import get_logger, LoggerName

logger = get_logger(LoggerName.ALGORITHM)

CONTINUOUS_COST = 1  # A constant that signals that the given project is in its continuous increment phase.
DISTRIBUTION_PARAMETER_COST = 100  # The amount of increase in each voter's budget at each iteration is budget/DISTRIBUTION_PARAMETER_COST.
# If DISTRIBUTION_PARAMETER_COST is larger, then the computation is more accurate, but requires longer time.
MAX_ROUNDS = 1000 # A constant that provides a safety net to prevent infinite loops


def equal_shares(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: float,
    bids: dict[int, dict[int, int]],
    tracker_callback = None
) -> tuple[dict[int, int], dict[int, dict[int, float]]]:
    """
    Implements the Method of Equal Shares (MES) algorithm for participatory budgeting.
    The algorithm distributes a budget among projects based on voter preferences, ensuring
    fair allocation by giving each voter an equal share of the budget initially.

    Args:
        voters (list[int]): List of voter IDs participating in the vote.
        projects_costs (dict[int, int]): Dictionary mapping project IDs to their minimum costs.
        budget (float): Total available budget to be distributed.
        bids (dict[int, dict[int, int]]): Nested dictionary where:
            - First level key: project ID
            - Second level key: voter ID
            - Value: amount bid by that voter for that project
        tracker_callback (Optional[Callable]): Callback function for tracking algorithm progress.

    Returns:
        tuple[dict[int, int], dict[int, dict[int, float]]]: A tuple containing:
            - winners_allocations: Dictionary mapping project IDs to their allocated costs
            - candidates_payments_per_voter: Nested dictionary showing how much each voter
              contributed to each project (project_id -> voter_id -> payment_amount)

    Examples:
        >>> # Simple example with three voters and two projects
        >>> voters = [1, 2, 3]
        >>> projects_costs = {101: 100, 102: 150}  # Project costs
        >>> budget = 300
        >>> bids = {
        ...     101: {1: 100, 2: 100, 3: 0},      # Voters 1 and 2 support project 101
        ...     102: {2: 150, 3: 150, 1: 0}       # Voters 2 and 3 support project 102
        ... }
        >>> winners, payments = equal_shares(voters, projects_costs, budget, bids)
        >>> winners
        {101: 100, 102: 150}  # Both projects funded
        >>> payments[101]  # Payments for project 101
        {1: 50, 2: 50, 3: 0}  # Voters 1 and 2 split the cost

    Notes:
        - Each voter starts with an equal share of the budget (budget / num_voters)
        - The algorithm iteratively tries to fund projects by:
            1. Finding projects with the highest effective support
            2. Distributing costs equally among supporting voters
            3. Gradually increasing voter budgets if needed
        - A project is funded if its supporting voters have enough remaining budget
        - The algorithm stops when either:
            - No more projects can be funded within budget constraints
            - The total cost would exceed the available budget

    Raises:
        ValueError: If project costs exceed available budgets or if cost distribution fails.
    """
    logger.debug(f'ES input:\n voters: {voters} \n projects_costs: {projects_costs} \n budget: {budget} \n bids: {bids}')
    projects = projects_costs.keys() # Get list of project IDs
    bids = remove_zero_bids(bids)
    bids = remove_invalid_bids(voters, bids) # Remove bids from invalid voters
    max_bid_for_project = find_max(bids)

    # Initialize a dict to track previous allocations
    previous_allocations = {pid: 0 for pid in projects}

    # Round the budget to ensure equal division among voters
    rounded_budget: float = int(budget / len(voters)) * len(voters)  
    logger.warning("\nRunning equal_shares: budget=%s, rounded to %s", budget, rounded_budget)

    # Run first round with initial budget
    logger.debug("Calling ESFB for the first time")
    winners_allocations, projects_costs_of_next_increase, candidates_payments_per_voter = equal_shares_fixed_budget(
        voters, projects_costs, rounded_budget, bids, max_bid_for_project, previous_allocations, tracker_callback
    )

    # Calculate total cost of chosen projects
    total_chosen_project_cost = sum(winners_allocations[c] for c in winners_allocations)
    logger.warning("total_chosen_project_cost=%s", total_chosen_project_cost)

    round_count = 0

    while True:
        round_count += 1
        logger.debug(f'round_count: {round_count}')
        if round_count > MAX_ROUNDS:
            logger.warning(
                f"Max rounds ({MAX_ROUNDS}) reached - forcing termination. "
                f"Consider adjusting DISTRIBUTION_PARAMETER_COST"
            )
            break
            
        # Check if current outcome is exhaustive
        is_exhaustive = True
        for candidate in projects:
            candidate_cost_of_next_increase = projects_costs_of_next_increase[candidate]
            # Check if we can fund more projects
            if (
                # Would stay within total budget
                (total_chosen_project_cost + candidate_cost_of_next_increase <= budget)
                # Would not exceed max bid for this project
                and (winners_allocations[candidate] + candidate_cost_of_next_increase <= max_bid_for_project[candidate])
                # Project has a positive cost for next increase
                and (candidate_cost_of_next_increase > 0)
            ):
                is_exhaustive = False
                logger.warning("Candidate %s is not fully funded - allocation is not exhaustive", candidate)
                break
            
        if is_exhaustive:
            logger.warning("allocation is exhaustive")
            # No more projects can be funded
            break

        # Update budget for next round
        updated_rounded_budget = rounded_budget + len(voters) * (
            budget / DISTRIBUTION_PARAMETER_COST
        )

        # Run another round with increased budget
        updated_winners_allocations, projects_costs_of_next_increase, updated_candidates_payments_per_voter = (
            equal_shares_fixed_budget(
                voters,
                projects_costs,
                updated_rounded_budget,
                bids,
                max_bid_for_project,
                previous_allocations,
                tracker_callback
            )
        )

        # Calculate new total cost
        total_chosen_project_cost = sum(updated_winners_allocations[c] for c in updated_winners_allocations)
        logger.warning("total_chosen_project_cost=%s", total_chosen_project_cost)

        # If we exceed budget, stop
        if total_chosen_project_cost > budget:
            logger.warning("total_chosen_project_cost is more than the budget %s; breaking", budget)
            break

        # Else, keep increasing the budget and continue
        rounded_budget = updated_rounded_budget
        winners_allocations = updated_winners_allocations
        candidates_payments_per_voter = updated_candidates_payments_per_voter
    
    # if tracker_callback is not None:
    #     # Get only funded projects sorted by allocation amount
    #     funded_projects = [(pid, amount) for pid, amount in winners_allocations.items() 
    #                       if amount > 0]
    #     funded_projects.sort(key=lambda x: x[1], reverse=True)
        
    #     # Track each funded project for visualization
    #     remaining_budget = budget
    #     voter_budgets = {v: budget/len(voters) for v in voters}
    #     previous_allocations = {v: budget/len(voters) for v in voters}
        
    #     for project_id, allocation in funded_projects:
    #         # Calculate effective votes for ALL projects
    #         effective_votes = {}
    #         for pid in projects_costs.keys():
    #             pid_supporters = len([v for v, bid in bids[pid].items() if bid > 0])
    #             effective_votes[str(pid)] = float(pid_supporters)
    
    #         # Get the payments each voter made for this project
    #         project_payments = candidates_payments_per_voter[project_id]

    #         # Update voter budgets for tracking
    #         for voter_id in voter_budgets:
    #             voter_payment = project_payments.get(voter_id, 0)
    #             voter_budgets[voter_id] -= voter_payment

    #         logger.debug(f'calling tracker_callback with:\n project_id: {project_id}, ')
    #         logger.debug(f"\nDEBUG equal_shares before tracker:")
    #         logger.debug(f"project_id: {project_id}")
    #         logger.debug(f"voter_budgets: {voter_budgets}")
    #         logger.debug(f"previous_allocations: {previous_allocations}")
    #         logger.debug(f"project_payments: {project_payments}")

    #         tracker_callback(
    #             project_id=project_id,
    #             cost=allocation,
    #             effective_votes=effective_votes,
    #             voter_budgets=voter_budgets,
    #             previous_allocations=previous_allocations.copy(),
    #             payments_per_voter=project_payments
    #         )

    #         # Update previous allocations for next round
    #         for voter_id in previous_allocations:
    #             previous_allocations[voter_id] = voter_budgets[voter_id]
            
    #         remaining_budget -= allocation

    logger.debug(f'ES output:\n winners_allocations: {winners_allocations} \n candidates_payments_per_voter: {candidates_payments_per_voter}')
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


def distribute_cost_among_voters(cost: float, voters_and_budgets: list[tuple[Any, float]]) -> list[tuple[Any, float]]:
    """
    :argument
        cost (int): the total cost of the project to be funded.
        voters_and_budgets: a list of pairs; each pair is (voter_id, voter_budget).
    :return
        a list of pairs; each pair is (voter_id, voter_contribution_to_funding).

    The cost is distributed as equally as possible; voters who have too little budget, pay all their budget.

    >>> distribute_cost_among_voters(66, [("a",33.), ("b",44.), ("c",55.)])
    [('a', 22.0), ('b', 22.0), ('c', 22.0)]
    >>> distribute_cost_among_voters(66, [("a",11.), ("b",44.), ("c",55.)])
    [('a', 11.0), ('b', 27.5), ('c', 27.5)]
    >>> distribute_cost_among_voters(66, [("b",44.), ("a",11.), ("c",55.)])
    [('a', 11.0), ('b', 27.5), ('c', 27.5)]
    >>> distribute_cost_among_voters(66, [("a",11.), ("b",25.), ("c",55.)])
    [('a', 11.0), ('b', 25.0), ('c', 30.0)]
    >>> distribute_cost_among_voters(66, [("a",11.), ("b",12.), ("c",13.)])
    Traceback (most recent call last):
    ...
    ValueError: Project not fully funded: cost=66, remaining_cost=30.0
    """
    voters_and_budgets = sorted(voters_and_budgets, key=lambda x: x[1])  # sort by ascending budget
    voters_and_contributions = []
    num_of_voters = len(voters_and_budgets)
    remaining_cost = cost
    for i, (voter, voter_budget) in enumerate(voters_and_budgets):
        if voter_budget * (num_of_voters - i) >= remaining_cost:
            voter_contribution = remaining_cost / (num_of_voters - i)
        else:
            voter_contribution = voter_budget
        voters_and_contributions.append((voter, voter_contribution))
        remaining_cost -= voter_contribution
    if remaining_cost > 1:
        raise ValueError(f"Project not fully funded: cost={cost}, remaining_cost={remaining_cost}")
    return voters_and_contributions


def equal_shares_fixed_budget(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: float,
    bids: dict[int, dict[int, int]],
    max_bid_for_project: dict,
    previous_allocations: dict[int, float],
    tracker_callback
) -> tuple[dict[int, int], dict[int, int], dict[int, dict[int, float]]]:
    """
    Core implementation of the Method of Equal Shares (MES) algorithm for a fixed budget round.
    This function executes a single round of the MES algorithm, allocating a fixed budget
    among projects based on voter preferences and available funds.

    Args:
        voters (list[int]): List of voter IDs participating in the vote.
        projects_costs (dict[int, int]): Dictionary mapping project IDs to their minimum costs.
        budget (float): Fixed budget available for this round.
        bids (dict[int, dict[int, int]]): Nested dictionary where:
            - First level key: project ID
            - Second level key: voter ID
            - Value: amount bid by that voter for that project
        max_bid_for_project (dict[int, int]): Dictionary mapping project IDs to their maximum
            allowable funding amounts.

    Returns:
        tuple[dict[int, int], dict[int, int], dict[int, dict[int, float]]]: A tuple containing:
            - winners_allocations: Dictionary mapping project IDs to their allocated costs
            - updated_cost: Dictionary mapping project IDs to their remaining costs for next increase
            - candidates_payments_per_voter: Nested dictionary showing how much each voter
              contributed to each project (project_id -> voter_id -> payment_amount)

    Notes:
        - The function operates on a fixed budget, unlike equal_shares which can increase budgets
        - Projects are selected based on their "effective vote count", which considers:
            1. Number of supporting voters
            2. Remaining budget of supporting voters
            3. Project cost
        - For each selected project:
            1. Cost is distributed equally among supporting voters when possible
            2. Voters with insufficient funds contribute their entire remaining budget
            3. Other voters make up the difference equally
        - The process continues until:
            1. No more projects can be afforded, or
            2. All projects have been funded

    Raises:
        ValueError: If costs cannot be distributed fairly among voters or if voter budgets
                   are insufficient for project costs.
    """
    logger.warning("\n  Running ESFB: budget=%s", budget)
    projects = projects_costs.keys()

    # Give each voter an equal share of the budget
    voters_budgets = {i: budget / len(voters) for i in voters}
    # logger.debug("  Initial voters_budgets: %s", voters_budgets)

    # Track how much each voter pays for each project
    candidates_payments_per_voter = {
        candidate: {voter: 0.0 for voter in inner_dict.keys()} for candidate, inner_dict in bids.items()
    }

    # Track remaining candidates and their supporter counts
    remaining_candidates = {
        candidate: len(bids[candidate])
        for candidate in projects
        if projects_costs[candidate] > 0 and len(bids[candidate]) > 0
    }  # remaining candidate -> previous effective vote count

    # Track how much is allocated to each project
    winners_allocations = {
        candidate: 0 for candidate in projects
    }  # Initialize amount invested in each winning projects

    # Keep track of bids and costs that can change during the process
    updated_bids = copy.deepcopy(bids)
    updated_cost = copy.deepcopy(projects_costs)

    while True:
        # Track current round's effective votes for all projects
        current_round_effective_votes = {}
        # debug_totals()
        best_candidates = []
        best_effective_vote_count = 0.0  # best = the max effective supporters in all projects

        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_candidates_sorted = {
            candidate: effective_vote_count
            for candidate, effective_vote_count in sorted(
                remaining_candidates.items(), key=lambda item: item[1], reverse=True
            )
        }

        # logger.debug(
        #     "Remaining candidates sorted by decreasing previous effective vote count:\n   %s",
        #     remaining_candidates_sorted,
        # )
        # logger.debug("Voters' budgets:\n   %s", voters_budgets)

        # Calculate effective votes for all remaining candidates
        for candidate, previous_effective_vote_count in remaining_candidates_sorted.items():
            # Skip if we already found better projects
            if previous_effective_vote_count < best_effective_vote_count:
                # logger.debug(
                #     "Candidate %s: Previous effective vote count (%s) < best_effective_vote_count (%s): breaking",
                #     candidate,
                #     previous_effective_vote_count,
                #     best_effective_vote_count,
                # )
                break

            # Check if supporters have enough money combined
            money_behind_candidate = sum(
                voters_budgets[i] for i in updated_bids[candidate].keys() if updated_bids[candidate][i] > 0
            )

            # Skip if project can't be afforded
            if money_behind_candidate < updated_cost[candidate]:
                # candidate is not affordable - The total amount of money is less than the candidate cost
                # logger.debug(
                #     "Candidate %s not affordable: supporters have %s but updated_cost = %s",
                #     candidate,
                #     money_behind_candidate,
                #     updated_cost[candidate],
                # )
                del remaining_candidates[candidate]
                # The candidate cannot be purchased, so remove him from the candidate list
                continue

            # Calculate the effective vote count of candidate
            # Sort supporters by their remaining budget (lowest to highest)
            # This helps handle cases where some supporters can't pay their full share
            sorted_approvers = {
                voter: voters_budgets[voter]
                for voter in sorted(updated_bids[candidate].keys(), key=lambda i: voters_budgets[i])
            }

            # Calculate how many "effective" voters support the project
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
                    # Calculate effective vote count:
                    # A measure of project support that considers both number of supporters and their ability to pay.
                    # Formula: project_cost / equal_payment_per_voter
                    # Higher value means stronger support.
                    effective_vote_count = updated_cost[candidate] / equal_payment
                    # Store the effective vote count for this project
                    current_round_effective_votes[str(candidate)] = effective_vote_count
                    if effective_vote_count > best_effective_vote_count:
                        best_effective_vote_count = effective_vote_count
                        best_candidates = [candidate]
                    elif effective_vote_count == best_effective_vote_count:
                        best_candidates.append(candidate)
                    break
            # logger.debug(
            #     "Candidate %s: cost %s; approvers and budgets=%s; effective_vote_count=%s",
            #     candidate,
            #     updated_cost[candidate],
            #     sorted_approvers,
            #     effective_vote_count,
            # )
        # logger.debug("best_candidates: %s", best_candidates)
        # No more affordable projects
        if not best_candidates:
            # logger.info("No remaining candidates are affordable.")
            break  # Break out of the outer "while True" loop

        # Break ties if multiple projects tied
        best_found = break_ties(updated_cost, updated_bids, best_candidates)
        # logger.debug("best_found after tie-breaking: %s", best_found)

        if len(best_found) > 1:
            raise Exception(
                f"Tie-breaking failed: tie between projects {best_found} "
                + "could not be resolved. Another tie-breaking needs to be added."
            )
        
        chosen_candidate = best_found[0]

        """
        After receiving the selected project, we reduce the cost of the selected project from the Update_bids list
        and create a new project with a "factor" cost, we filter its data using the
        filter_bids function. Then they check whether the total price of the project
        does not exceed the highest price they chose.
        and update "remaining" with the number of voters who chose it at the new price. and continue the while loop.
        """

        chosen_candidate_max_bid = max_bid_for_project[chosen_candidate]
        chosen_candidate_cost = updated_cost[chosen_candidate]
        chosen_candidate_bids = updated_bids[chosen_candidate]
        # logger.debug(
        #     "Chosen project: %s, current cost: %s, max bid: %s, effective vote count: %s",
        #     chosen_candidate,
        #     chosen_candidate_cost,
        #     chosen_candidate_max_bid,
        #     best_effective_vote_count,
        # )
        # logger.debug("Updated bids: %s", updated_bids)

        # Calculate project cost
        if chosen_candidate_cost == CONTINUOUS_COST:
            positive_bids = {
                voter: bid for voter, bid in chosen_candidate_bids.items() if bid > 0 and voters_budgets[voter] > 0
            }
            """
            The chosen project is in its continuous phase.
             We increase its allocation up to one of the following thresholds:
            1. The allocation attains the maximum possible cost for the project:
               chosen_candidate_max_bid
            2. The addition attains the smallest bid of a supporter:
               min(bid for voter, bid in positive_bids.items())
            3. The addition attains the sum of budgets of all supporters.
            """
            chosen_candidate_cost = min(
                chosen_candidate_max_bid - winners_allocations[chosen_candidate],
                min(bid for voter, bid in positive_bids.items()),
                sum(voters_budgets[voter] for voter, bid in positive_bids.items()),
            )
            # logger.debug(
            #     "Chosen project is now in the continuous phase - adding %s", chosen_candidate_cost
            # )
            explanation_string_format = "Funding %s with additional %s has %s effective vote count"
        else:
            explanation_string_format = "Funding %s with the minimum amount %s has %s effective vote count"


        # Deducts from the voters_budget of each voter who chose the current
        # project the relative part for the current project
        # Update voter budgets and track payments
        voters_and_budgets = [(voter, voters_budgets[voter]) for voter in chosen_candidate_bids.keys()]
        voters_and_contributions = distribute_cost_among_voters(chosen_candidate_cost, voters_and_budgets)
        for voter, voter_payment in voters_and_contributions:
            # logger.debug("Voter %s contributes %s", voter, voter_payment)
            voters_budgets[voter] -= voter_payment
            candidates_payments_per_voter[chosen_candidate][voter] += voter_payment
        winners_allocations[chosen_candidate] += chosen_candidate_cost

        # check if the curr cost + total update codt <= max value for this projec
        # logger.info(" total project price   = %s", winners_total_cost[chosen_candidate])

        # Update remaining candidates
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
            explanation_string_format += ". New allocation is %s. New effective vote count is %s"
            new_effective_vote_count = remaining_candidates[chosen_candidate]
        else:
            updated_cost[chosen_candidate] = 0
            del remaining_candidates[chosen_candidate]
            explanation_string_format += "    Candidate now has the maximum possible allocation: %s. New effective vote count is %s"
            new_effective_vote_count = 0

        # logger.info(
        #     explanation_string_format,
        #     chosen_candidate,
        #     chosen_candidate_cost,
        #     best_effective_vote_count,
        #     winners_allocations[chosen_candidate],
        #     new_effective_vote_count
        # )

    if tracker_callback is not None:
        # Get only funded projects sorted by allocation amount
        funded_projects = [(pid, amount) for pid, amount in winners_allocations.items() 
                          if amount > 0]
        funded_projects.sort(key=lambda x: x[1], reverse=True)
        
        # Track each funded project for visualization
        remaining_budget = budget
        voter_budgets = {v: budget/len(voters) for v in voters}
        previous_voter_budgets = {v: budget/len(voters) for v in voters}
        
        for project_id, total_allocation in funded_projects:
            # Calculate the delta between current and previous allocation
            delta_allocation = total_allocation - previous_allocations[project_id]
            previous_allocations[project_id] = total_allocation  # Update for next time

            # Calculate effective votes for ALL projects
            effective_votes = {}
            for pid in projects_costs.keys():
                pid_supporters = len([v for v, bid in bids[pid].items() if bid > 0])
                effective_votes[str(pid)] = float(pid_supporters)

            # Get the payments each voter made for this project
            project_payments = candidates_payments_per_voter[project_id]

            # Update voter budgets for tracking
            for voter_id in voter_budgets:
                voter_payment = project_payments.get(voter_id, 0)
                voter_budgets[voter_id] -= voter_payment

            # logger.debug(f'calling tracker_callback with:')
            # logger.debug(f"project_id: {project_id}")
            # logger.debug(f"delta_allocation: {delta_allocation}")
            # logger.debug(f"effective_votes: {effective_votes}")
            # logger.debug(f"voter_budgets: {voter_budgets}")
            # logger.debug(f"previous_voter_budgets: {previous_voter_budgets}")
            # logger.debug(f"project_payments: {project_payments}")

            tracker_callback(
                project_id=project_id,
                cost=delta_allocation,
                effective_votes=effective_votes,
                voter_budgets=voter_budgets,
                previous_allocations=previous_voter_budgets.copy(),
                payments_per_voter=project_payments
            )

            # Update previous budgets for next round
            previous_voter_budgets = voter_budgets.copy()
            remaining_budget -= delta_allocation

    logger.info("ESFB | winners_allocations: %s", winners_allocations)
    logger.info("ESFB | Cost for next increase: %s", updated_cost)
    return winners_allocations, updated_cost, candidates_payments_per_voter
