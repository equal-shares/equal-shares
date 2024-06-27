# equal_shares.py
import copy
import logging
import doctest


from utils import find_max, filter_bids

logger = logging.getLogger("equal_shares_logger")


def equal_shares(voters: list, projects: list, cost: dict, approvers: dict, budget: int, bids: dict, budget_increment_per_project: int):


    '''
    # T.0
    >>> voters = [1, 2, 3, 4, 5]  # Voters
    >>> projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    >>> cost = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    >>> approvers = {1: [1, 2, 4], 2: [2, 5], 3: [1, 5], 4: [3, 4], 5: [2, 3, 5], 6: [2, 5], 7: [1, 4], 8: [2, 5], 9: [1, 3, 5], 10: [2, 3]}
    >>> bids = { 1: {1: 100, 2: 100, 4: 100},2: {2: 150, 5: 150},3: {1: 200, 5: 200}, 4: {3: 250, 4: 250, },5: {2: 300, 3: 300, 5: 300},6: {2: 350, 5: 350}, 7: {1: 400, 4: 400, },8: {2: 450, 5: 450},9: {1: 500, 3: 500,5: 500},10:{2: 550, 3: 550}}
    >>> budget = 900  # Total budget
    >>> budget_increment_per_project = 10
    >>> equal_shares(voters, projects, cost, approvers,budget, bids,budget_increment_per_project)
    ([1, 3, 4, 5], {1: 100, 2: 0, 3: 200, 4: 250, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, {1: {1: 33.333333333333336, 2: 33.333333333333336, 4: 33.333333333333336}, 2: {2: 0, 5: 0}, 3: {1: 108.0, 5: 0}, 4: {3: 0, 4: 158.0}, 5: {2: 100.0, 3: 100.0, 5: 100.0}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0}, 8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}})'''
  

    max_cost_for_project = find_max(bids)
    chosen_project, chosen_project_cost, update_cost,budget_per_voter = equal_shares_fixed_budget(voters, projects, cost, approvers, budget, bids, budget_increment_per_project,max_cost_for_project)

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
            # and total project_cost + curr project_cost <= max value for curr project, if true thr price of the project can be increased

            if (project not in chosen_project and total_chosen_project_cost + cost[project] <= budget) or \
                    (project in chosen_project and total_chosen_project_cost + project_cost <= budget and
                     chosen_project_cost[project] + project_cost <= max_value_project):
                is_exhaustive = False

                break
        # if so, stop
        if is_exhaustive:
            break
        # would the next highest voters_budget work?
        update_voters_budget = voters_budget + len(voters)  # Add 1 to each voter's voters_budget
        logger.info("  call fix voters_budget   = %s B= %s, %s", total_chosen_project_cost, budget, update_voters_budget)
        update_chosen_project, update_chosen_project_cost, update_cost, update_budget_per_voter = equal_shares_fixed_budget(voters, projects, cost, approvers, update_voters_budget, bids, budget_increment_per_project,max_cost_for_project)
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

    return chosen_project, chosen_project_cost,budget_per_voter



'''
break ties
first the min cost project
second the max voter for project
Ensure there is only one remaining project, third the min index project
'''
def break_ties(cost: dict, approvers: dict, bids: list):
    remaining = bids.copy()
    best_cost = min(cost[c] for c in remaining)  # first the min cost project
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(approvers[c]) for c in remaining)  # second the max voter for project
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    remaining = [min(remaining)]  # Ensure there is only one remaining project, third the min index project
    return remaining



def equal_shares_fixed_budget(voters: list, projects: list, cost: dict, approvers: dict, budget: int, bids: dict, budget_increment_per_project:int,max_cost_for_project:dict):

    voters_budget = {i: budget / len(voters) for i in voters}

    remaining = {}  # remaining candidate -> previous effective vote count

    budget_per_voter = {}
    for outer_key, inner_dict in bids.items():
        # Initialize the inner dictionary with values set to 0
        budget_per_voter[outer_key] = {inner_key: 0 for inner_key in inner_dict.keys()}

    for c in projects:
        if cost[c] > 0 and len(approvers[c]) > 0:
            remaining[c] = len(approvers[c])

    # logger.info("Remaining --> the number of relevant vote for any project remaining=%s", remaining)

    winners = []

    update_bids = copy.deepcopy(bids)
    update_approvers = copy.deepcopy(approvers)
    update_cost = copy.deepcopy(cost)
    winners_total_cost = {key: 0 for key in projects}

    while True:

        best = []
        best_eff_vote_count = 0

        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)

        for c in remaining_sorted:
            previous_eff_vote_count = remaining[c]
            if previous_eff_vote_count < best_eff_vote_count:
                # c cannot be better than the best so far
                # logger.info("c cannot be better than the best so far c=%s", c)

                break
            money_behind_now = sum(voters_budget[i] for i in update_approvers[c])
            if money_behind_now < update_cost[c]:
                # c is not affordable
                del remaining[c]
                # logger.info("c is not affordable c=%s, update_cost for c=%s ", update_cost[c])
                continue
            # calculate the effective vote count of c
            update_approvers[c].sort(key=lambda i: voters_budget[i])
            paid_so_far = 0
            denominator = len(update_approvers[c])
            for i in update_approvers[c]:
                # compute payment if remaining approvers pay equally
                max_payment = (update_cost[c] - paid_so_far) / denominator
                eff_vote_count = update_cost[c] / max_payment
                if max_payment > voters_budget[i]:
                    # i cannot afford the payment, so pays entire remaining voters_budget
                    paid_so_far += voters_budget[i]
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    remaining[c] = int(eff_vote_count)
                    if eff_vote_count > best_eff_vote_count:
                        best_eff_vote_count = eff_vote_count
                        best = [c]
                    elif eff_vote_count == best_eff_vote_count:
                        best.append(c)

                    break
        if not best:
        # logger.info(" no remaining candidates are affordable ,best = %s", best)

            break
        best = break_ties(update_cost, update_approvers, best)
        # logger.info(" after vreak ties ,best  = %s", best)

        if len(best) > 1:
            raise Exception(f"Tie-breaking failed: tie between projects {best} " + \
                            "could not be resolved. Another tie-breaking needs to be added.")
        best = best[0]
        winners.append(best)
        winners = set(winners)
        winners = list(winners)

        logger.info("  ,winners  = %s", winners)



        """

            After receiving the selected project, we reduce the cost of the selected project from the Update_bids list
            and create a new project with a "factor" cost, we filter its data using the 
            filter_bids function.Then they check whether the total price of the project does not exceed the highest price they chose.
            and update "remaining" with the number of voters who chose it at the new price. and continue the while loop.

        """

        # the project curr id number and  cost

        curr_project_id = best
        curr_project_cost = update_cost[best]

        logger.info(" id and cost for the chosen project   = %s, %s", curr_project_id, curr_project_cost)

        # Find the highest choice for the current project
        max_value_project = max_cost_for_project[curr_project_id]
        # Deducts from the voters_budget of each voter who chose the current project the relative part for the current project

        best_max_payment = curr_project_cost / best_eff_vote_count


        for i in update_bids[curr_project_id].keys():
            if voters_budget[i] > best_max_payment:
                voters_budget[i] -= best_max_payment
                budget_per_voter[curr_project_id][i] = budget_per_voter[curr_project_id][i] + best_max_payment
            else:
                voters_budget[i] = 0

        # chack if the curr cost + total update codt <= max value for this projec
        # logger.info(" total project price   = %s", winners_total_cost[curr_project_id])

        if winners_total_cost[curr_project_id] + curr_project_cost <= max_value_project:

            filter_bids(update_bids, update_approvers, curr_project_id, curr_project_cost, budget_increment_per_project, update_cost)

            winners_total_cost[curr_project_id] = winners_total_cost[curr_project_id] + curr_project_cost

            # Updates the remaining list in the number of voters after updating the price of the project
            remaining[curr_project_id] = len(update_bids[curr_project_id].keys())

        else:

            update_cost[curr_project_id] = 0
            del remaining[curr_project_id]

    # logger.info("winners return  = %s", winners)
    return winners, winners_total_cost, update_cost,budget_per_voter



if __name__ == "__main__":
    import doctest

logger.setLevel(logging.WARNING)  # Turn off "info" log messages
print(doctest.testmod())
logger.setLevel(logging.INFO)  # Turn on "info" log messages
logger.addHandler(logging.StreamHandler())