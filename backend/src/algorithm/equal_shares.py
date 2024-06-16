# equal_shares.py
import copy
import logging
import doctest

# Your test code here

from utils import find_max, filter_bids

logger = logging.getLogger("equal_shares_logger")


def equal_shares(voters, projects, cost, approvers, budget, bids, budget_increment_per_project):


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
    ([1, 3, 4, 5], {1: 100, 2: 0, 3: 200, 4: 250, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, {1: {1: 70.0, 2: 70.0, 4: 70.0}, 2: {2: 0, 5: 0}, 3: {1: 100.0, 5: 100.0}, 4: {3: 0, 4: 134.33333333333331}, 5: {2: 203.33333333333331, 3: 203.33333333333331, 5: 203.33333333333331}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0}, 8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}})

    '''

    max_cost_for_project = find_max(bids)
    chosen_project, chosen_project_cost, update_cost, budget_per_voter = equal_shares_fixed_budget(
        voters, projects, cost, approvers, budget, bids, budget_increment_per_project, max_cost_for_project)

    voters_budget = int(budget / len(voters)) * len(voters)
    total_chosen_project_cost = sum(chosen_project_cost[c] for c in chosen_project_cost)

    while True:
        is_exhaustive = True
        for project in projects:
            max_value_project = max_cost_for_project[project]
            project_cost = update_cost[project]

            if (project not in chosen_project and total_chosen_project_cost + cost[project] <= budget) or \
                    (project in chosen_project and total_chosen_project_cost + project_cost <= budget and
                     chosen_project_cost[project] + project_cost <= max_value_project):
                is_exhaustive = False
                break

        if is_exhaustive:
            break

        update_voters_budget = voters_budget + len(voters)
        update_chosen_project, update_chosen_project_cost, update_cost, update_budget_per_voter = equal_shares_fixed_budget(
            voters, projects, cost, approvers, update_voters_budget, bids, budget_increment_per_project,
            max_cost_for_project)

        total_chosen_project_cost = sum(update_chosen_project_cost[c] for c in update_chosen_project_cost)

        if total_chosen_project_cost <= budget:
            voters_budget = update_voters_budget
            chosen_project = update_chosen_project
            chosen_project_cost = update_chosen_project_cost
            budget_per_voter = update_budget_per_voter
        else:
            break

    return chosen_project, chosen_project_cost, budget_per_voter


def break_ties(cost, approvers, bids):
    remaining = bids.copy()
    best_cost = min(cost[c] for c in remaining)
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(approvers[c]) for c in remaining)
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    remaining = [min(remaining)]
    return remaining


def equal_shares_fixed_budget(voters, projects, cost, approvers, budget, bids, budget_increment_per_project,
                              max_cost_for_project):


    '''
    # T.0
    >>> voters = [1, 2, 3, 4, 5]  # Voters
    >>> projects = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Project IDs
    >>> cost = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    >>> approvers = {1: [1, 2, 4], 2: [2, 5], 3: [1, 5], 4: [3, 4], 5: [2, 3, 5], 6: [2, 5], 7: [1, 4], 8: [2, 5], 9: [1, 3, 5], 10: [2, 3]}
    >>> bids = { 1: {1: 100, 2: 100, 4: 100},2: {2: 150, 5: 150},3: {1: 200, 5: 200}, 4: {3: 250, 4: 250, },5: {2: 300, 3: 300, 5: 300},6: {2: 350, 5: 350}, 7: {1: 400, 4: 400, },8: {2: 450, 5: 450},9: {1: 500, 3: 500,5: 500},10:{2: 550, 3: 550}}
    >>> budget = 900  # Total budget
    >>> budget_increment_per_project = 10
    >>> max_cost_for_project = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}
    >>> equal_shares_fixed_budget(voters, projects, cost, approvers,budget, bids,budget_increment_per_project,max_cost_for_project)
    ([1, 5], {1: 100, 2: 0, 3: 0, 4: 0, 5: 300, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}, {1: 0, 2: 150, 3: 200, 4: 250, 5: 310, 6: 350, 7: 400, 8: 450, 9: 500, 10: 550}, {1: {1: 70.0, 2: 70.0, 4: 70.0}, 2: {2: 0, 5: 0}, 3: {1: 0, 5: 0}, 4: {3: 0, 4: 0}, 5: {2: 100.0, 3: 100.0, 5: 100.0}, 6: {2: 0, 5: 0}, 7: {1: 0, 4: 0}, 8: {2: 0, 5: 0}, 9: {1: 0, 3: 0, 5: 0}, 10: {2: 0, 3: 0}})
    '''

    voters_budget = {i: budget / len(voters) for i in voters}
    remaining = {c: len(approvers[c]) for c in projects if cost[c] > 0 and len(approvers[c]) > 0}
    budget_per_voter = {outer_key: {inner_key: 0 for inner_key in inner_dict.keys()} for outer_key, inner_dict in
                        bids.items()}

    winners = []
    update_bids = copy.deepcopy(bids)
    update_approvers = copy.deepcopy(approvers)
    update_cost = copy.deepcopy(cost)
    winners_total_cost = {key: 0 for key in projects}

    while True:
        best = []
        best_eff_vote_count = 0
        remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)

        for c in remaining_sorted:
            previous_eff_vote_count = remaining[c]
            if previous_eff_vote_count < best_eff_vote_count:
                break
            money_behind_now = sum(voters_budget[i] for i in update_approvers[c])
            if money_behind_now < update_cost[c]:
                del remaining[c]
                continue

            update_approvers[c].sort(key=lambda i: voters_budget[i])
            paid_so_far = 0
            denominator = len(update_approvers[c])
            for i in update_approvers[c]:
                max_payment = (update_cost[c] - paid_so_far) / denominator
                eff_vote_count = update_cost[c] / max_payment
                if max_payment > voters_budget[i]:
                    paid_so_far += voters_budget[i]
                    denominator -= 1
                else:
                    remaining[c] = int(eff_vote_count)
                    if eff_vote_count > best_eff_vote_count:
                        best_eff_vote_count = eff_vote_count
                        best = [c]
                    elif eff_vote_count == best_eff_vote_count:
                        best.append(c)
                    break
        if not best:
            break

        best = break_ties(update_cost, update_approvers, best)
        if len(best) > 1:
            raise Exception(
                f"Tie-breaking failed: tie between projects {best} could not be resolved. Another tie-breaking needs to be added.")
        best = best[0]
        winners.append(best)
        winners = list(set(winners))

        curr_project_id = best
        curr_project_cost = update_cost[best]
        max_value_project = max_cost_for_project[curr_project_id]
        best_max_payment = curr_project_cost / best_eff_vote_count

        for i in update_bids[curr_project_id].keys():
            if voters_budget[i] > best_max_payment:
                voters_budget[i] -= best_max_payment
                budget_per_voter[curr_project_id][i] += best_max_payment
            else:
                voters_budget[i] = 0

        if winners_total_cost[curr_project_id] + curr_project_cost <= max_value_project:
            filter_bids(update_bids, update_approvers, curr_project_id, curr_project_cost, budget_increment_per_project,
                        update_cost)
            winners_total_cost[curr_project_id] += curr_project_cost
            remaining[curr_project_id] = len(update_bids[curr_project_id].keys())
        else:
            update_cost[curr_project_id] = 0
            del remaining[curr_project_id]

    return winners, winners_total_cost, update_cost, budget_per_voter



if __name__ == "__main__":
    import doctest

logger.setLevel(logging.WARNING)  # Turn off "info" log messages
print(doctest.testmod())
logger.setLevel(logging.INFO)  # Turn on "info" log messages
logger.addHandler(logging.StreamHandler())