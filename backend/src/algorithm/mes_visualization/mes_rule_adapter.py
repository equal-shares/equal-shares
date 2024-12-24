"""
Custom implementation of Method of Equal Shares (MES) that bridges 
pabutools interface with our implementation.
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from gmpy2 import mpq

from pabutools.election import Instance, AbstractProfile, Cost_Sat
from pabutools.rules import BudgetAllocation
from pabutools.rules.mes.mes_details import MESAllocationDetails, MESIteration, MESProjectDetails

from src.algorithm.equal_shares import equal_shares


@dataclass
class MESInput:
    """Normalized input data for MES algorithm."""
    voters: List[int]
    projects_costs: Dict[int, int]
    budget: float
    bids: Dict[int, Dict[int, int]]
    projects_meta: Dict[int, Any]


def convert_pabutools_input(instance: Instance, profile: AbstractProfile) -> MESInput:
    """Convert pabutools input format to algorithm format."""
    # Extract voters
    voters = list(range(profile.num_ballots()))
    
    # Extract project costs using max_points
    projects_costs = {}
    for project in instance:
        project_id = int(project.name)
        meta = instance.project_meta.get(str(project_id), {})
        # Use max_points if available, otherwise use cost
        projects_costs[project_id] = meta.get('max_points', float(project.cost))
    
    # Extract bids from original votes
    bids = {}
    original_votes = getattr(profile, '_original_votes', None)
    if original_votes:
        for vote_data in original_votes:
            voter_id = vote_data.voter.voter_id
            for project_vote in vote_data.projects:
                project_id = project_vote.project_id
                if project_id not in bids:
                    bids[project_id] = {}
                bids[project_id][voter_id] = project_vote.points if project_vote.points > 0 else 0
    else:
        # Fallback to binary approval if no original votes
        for project in instance:
            project_id = int(project.name)
            bids[project_id] = {}
            for voter_idx, ballot in enumerate(profile):
                bids[project_id][voter_idx] = 1 if project in ballot else 0

    return MESInput(
        voters=voters,
        projects_costs=projects_costs,
        budget=float(instance.budget_limit),
        bids=bids,
        projects_meta={int(p.name): p for p in instance}
    )

def create_mes_iteration(round_info, project, instance, profile) -> MESIteration:
    """Create MES iteration details for visualization."""
    # Skip if this is a budget update round or has no actual cost
    if round_info.is_budget_update or round_info.cost == 0:
        return None

    iteration = MESIteration()
    
    # Find the project from instance
    project_obj = next(p for p in instance if int(p.name) == round_info.selected_project)
    
    # Calculate supporter indices for each project
    voter_indices = []
    for voter_idx, ballot in enumerate(profile):
        if project_obj in ballot:
            voter_indices.append(voter_idx)
    
    # Create a mapping of Project objects to their effective votes
    effective_votes_map = {}
    for proj in instance:
        proj_id = int(proj.name)
        if proj_id in round_info.effective_votes:
            effective_votes_map[proj] = round_info.effective_votes[proj_id]
    
    # Add required properties to Project object
    project_obj.supporter_indices = voter_indices
    project_obj.affordability = 1.0 / effective_votes_map.get(project_obj, 1)
    project_obj.effective_vote_count = effective_votes_map.get(project_obj, 0)
    
    # Create MESProjectDetails for the selected project
    project_details = MESProjectDetails(project_obj, iteration)
    project_details.affordability = project_obj.affordability
    project_details.effective_vote_count = project_obj.effective_vote_count
    
    # Set both the raw project and its details
    iteration.selected_project = project_obj
    iteration.append(project_details)
    
    # Add details for unselected projects
    for other_proj in instance:
        if int(other_proj.name) != round_info.selected_project:
            # Calculate supporter indices for unselected project
            other_voter_indices = []
            for voter_idx, ballot in enumerate(profile):
                if other_proj in ballot:
                    other_voter_indices.append(voter_idx)
                    
            # Add properties to unselected Project
            other_proj.supporter_indices = other_voter_indices
            other_proj.affordability = 1.0 / effective_votes_map.get(other_proj, 1)
            other_proj.effective_vote_count = effective_votes_map.get(other_proj, 0)
            
            # Create and add details
            other_details = MESProjectDetails(other_proj, iteration)
            other_details.affordability = other_proj.affordability
            other_details.effective_vote_count = other_proj.effective_vote_count
            iteration.append(other_details)
    
    # Set budget information
    iteration.voters_budget = list(round_info.voter_budgets.values())
    iteration.voters_budget_after_selection = list(round_info.voter_budgets.values())
    
    return iteration

def method_of_equal_shares(
    instance: Instance,
    profile: AbstractProfile,
    sat_class: Optional[type] = None,
    analytics: bool = False,
    verbose: bool = False,
    **kwargs
) -> BudgetAllocation:
    # Convert input
    input_data = convert_pabutools_input(instance, profile)
    
    # Run algorithm and get winners
    winners, payments = equal_shares(
        voters=input_data.voters,
        projects_costs=input_data.projects_costs,
        budget=input_data.budget,
        bids=input_data.bids,
        tracker_callback=None
    )

    print(f"DEBUG - Winners and their allocations: {winners}")

    # Create allocation with the allocated amounts
    allocation = BudgetAllocation()
    
    if analytics:
        details = MESAllocationDetails([1] * len(input_data.voters))
        project_iterations = []
        
        # Calculate initial voter budgets
        initial_budget_per_voter = input_data.budget / len(input_data.voters)
        remaining_budgets = {voter: initial_budget_per_voter for voter in input_data.voters}
        
        # Create iterations for winning projects
        for project_id, allocated_cost in winners.items():
            if allocated_cost > 0:
                project = next(p for p in instance if int(p.name) == project_id)
                
                # Update the project's cost to reflect actual allocation
                project.cost = mpq(str(allocated_cost))
                
                iteration = MESIteration()
                
                # Get supporter indices
                voter_indices = []
                for voter_idx, ballot in enumerate(profile):
                    if project in ballot:
                        voter_indices.append(voter_idx)
                        # Update remaining budget
                        voter_id = input_data.voters[voter_idx]
                        payment = payments.get(project_id, {}).get(voter_id, 0)
                        remaining_budgets[voter_id] -= payment
                
                # Set required properties
                project.supporter_indices = voter_indices
                project.affordability = allocated_cost / (len(voter_indices) if voter_indices else 1)
                project.effective_vote_count = len(voter_indices)
                
                # Create project details with actual allocation
                project_details = MESProjectDetails(project, iteration)
                project_details.allocation = allocated_cost
                project_details.affordability = project.affordability
                project_details.effective_vote_count = project.effective_vote_count
                
                # Set iteration details
                iteration.selected_project = project
                iteration.voters_budget = list(remaining_budgets.values())
                iteration.voters_budget_after_selection = list(remaining_budgets.values())
                
                iteration.append(project_details)
                project_iterations.append(iteration)
                allocation.append(project)
        
        details.iterations = project_iterations
        details.allocations = winners
        allocation.details = details
    else:
        # Simple allocation without analytics
        for project_id, allocated_cost in winners.items():
            if allocated_cost > 0:
                project = next(p for p in instance if int(p.name) == project_id)
                project.cost = mpq(str(allocated_cost))
                allocation.append(project)

    return allocation
