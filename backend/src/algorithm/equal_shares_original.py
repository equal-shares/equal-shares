# ORiginal code taken from this link:
# https://equalshares.net/implementation/computation

# Completion method: Add1U


def equal_shares(voters: list, projects: list, cost: dict, approvers: dict, total_budget: int) -> list:
    """
    Computes the Method of Equal Shares for Participatory Budgeting.

    Args:
        voters (list): A list of voter names.
        projects (list): A list of project IDs.
        cost (dict): A dictionary mapping project IDs to their respective costs.
        approvers (dict): A dictionary mapping project IDs to the list of voters who approve them.
        total_budget (int): The total budget available.

    Returns:
        list: A list of project IDs that are selected by the Method of Equal Shares.

    Example:
        >>> equal_shares(
        >>>    voters=["v1", "v2", "v3"],
        >>>    projects=["p1", "p2", "p3"],
        >>>    cost={"p1": 100, "p2": 50, "p3": 50},
        >>>    approvers={"p1": ["v1", "v2"], "p2": ["v1"], "p3": ["v3"]},
        >>>    total_budget=150)
        ["p1", "p3"]

    """
    mes = equal_shares_fixed_budget(voters, projects, cost, approvers, total_budget)
    # add1 completion
    # start with integral per-voter budget
    budget = int(total_budget / len(voters)) * len(voters)
    current_cost = sum(cost[c] for c in mes)
    while True:
        # is current outcome exhaustive?
        is_exhaustive = True
        for extra in projects:
            if extra not in mes and current_cost + cost[extra] <= total_budget:
                is_exhaustive = False
                break
        # if so, stop
        if is_exhaustive:
            break
        # would the next highest budget work?
        next_budget = budget + len(voters)
        next_mes = equal_shares_fixed_budget(voters, projects, cost, approvers, next_budget)
        current_cost = sum(cost[c] for c in next_mes)
        if current_cost <= total_budget:
            # yes, so continue with that budget
            budget = next_budget
            mes = next_mes
        else:
            # no, so stop
            break
    # utilitarian completion after add1 (as part of add1u)
    mes = utilitarian_completion(voters, projects, cost, approvers, total_budget, mes)
    return mes


def utilitarian_completion(
    voters: list, projects: list, cost: dict, approvers: dict, total_budget: int, already_winners: list
) -> list:
    winners = list(already_winners)
    cost_so_far = sum(cost[c] for c in winners)
    # sort candidates by score
    sorted_projects = sorted(projects, key=lambda c: len(approvers[c]), reverse=True)
    # for each candidate in order of decreasing score,
    # try to add it to the committee
    for c in sorted_projects:
        if c in winners or cost_so_far + cost[c] > total_budget:
            continue
        winners.append(c)
        cost_so_far += cost[c]
    return winners


def break_ties(voters: list, projects: list, cost: dict, approvers: dict, choices: list) -> list:
    remaining = choices.copy()
    best_count = max(len(approvers[c]) for c in remaining)
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    remaining = [min(remaining)]  # Ensure there is only one remaining project, third the min index project
    return remaining


def equal_shares_fixed_budget(voters: list, projects: list, cost: dict, approvers: dict, total_budget: int) -> list:
    budget = {i: total_budget / len(voters) for i in voters}
    remaining = {}  # remaining candidate -> previous effective vote count
    for c in projects:
        if cost[c] > 0 and len(approvers[c]) > 0:
            remaining[c] = len(approvers[c])
    winners = []
    while True:
        best = []
        best_eff_vote_count = 0
        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)
        for c in remaining_sorted:
            previous_eff_vote_count = remaining[c]
            if previous_eff_vote_count < best_eff_vote_count:
                # c cannot be better than the best so far
                break
            money_behind_now = sum(budget[i] for i in approvers[c])
            if money_behind_now < cost[c]:
                # c is not affordable
                del remaining[c]
                continue
            # calculate the effective vote count of c
            approvers[c].sort(key=lambda i: budget[i])
            paid_so_far = 0.0
            denominator = len(approvers[c])
            for i in approvers[c]:
                # compute payment if remaining approvers pay equally
                max_payment = (cost[c] - paid_so_far) / denominator
                eff_vote_count = cost[c] / max_payment
                if max_payment > budget[i]:
                    # i cannot afford the payment, so pays entire remaining budget
                    paid_so_far += budget[i]
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    remaining[c] = eff_vote_count
                    if eff_vote_count > best_eff_vote_count:
                        best_eff_vote_count = eff_vote_count
                        best = [c]
                    elif eff_vote_count == best_eff_vote_count:
                        best.append(c)
                    break
        if not best:
            # no remaining candidates are affordable
            break
        best = break_ties(voters, projects, cost, approvers, best)
        if len(best) > 1:
            raise Exception(
                f"Tie-breaking failed: tie between projects {best} could not be resolved. "
                f"Another tie-breaking needs to be added."
            )
        best = best[0]
        winners.append(best)
        del remaining[best]
        # charge the approvers of best
        best_max_payment = cost[best] / best_eff_vote_count
        for i in approvers[best]:
            if budget[i] > best_max_payment:
                budget[i] -= best_max_payment
            else:
                budget[i] = 0
    return winners
