"""
Custom implementation of Method of Equal Shares (MES) that bridges 
pabutools interface with our implementation.
"""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass

from pabutools.election import Instance, AbstractProfile, Cost_Sat
from pabutools.rules import BudgetAllocation
from pabutools.rules.mes.mes_details import MESAllocationDetails, MESIteration, MESProjectDetails

from src.algorithm.equal_shares import equal_shares
from src.algorithm.mes_visualization.round_tracker import RoundTracker
from src.algorithm.mes_visualization.pabutools_adapter import CustomBudgetAllocation

@dataclass
class MESInput:
    """Normalized input data for MES algorithm."""
    voters: List[int]
    projects_costs: Dict[int, int]
    budget: float
    bids: Dict[int, Dict[int, int]]
    projects_meta: Dict[int, Any]

def convert_pabutools_input(
    instance: Instance,
    profile: AbstractProfile
) -> MESInput:
    """Convert pabutools input format to our algorithm format."""
    # Extract voters
    voters = list(range(profile.num_ballots()))
    
    # Extract project costs
    projects_costs = {
        int(project.name): float(project.cost)
        for project in instance
    }
    
    # Extract bids using original vote points
    bids = {}
    original_votes = getattr(profile, '_original_votes', None)
    
    if original_votes:
        # Use original vote points
        for vote_data in original_votes:
            voter_id = vote_data.voter.voter_id
            for project_vote in vote_data.projects:
                project_id = project_vote.project_id
                if project_id not in bids:
                    bids[project_id] = {}
                bids[project_id][voter_id] = project_vote.points if project_vote.points > 0 else 0
    else:
        # Fallback to binary approval if original votes not available
        for project in instance:
            project_id = int(project.name)
            bids[project_id] = {}
            for voter_idx, ballot in enumerate(profile):
                bids[project_id][voter_idx] = 1 if project in ballot else 0

    print(f'bids: {bids}')

    return MESInput(
        voters=voters,
        projects_costs=projects_costs,
        budget=float(instance.budget_limit),
        bids=bids,
        projects_meta={
            int(p.name): p for p in instance
        }
    )

def create_mes_iteration(round_info, project, instance, profile) -> MESIteration:
    """Create MES iteration details for visualization."""
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
    """
    Custom implementation of Method of Equal Shares that integrates with pabutools.
    """
    # Convert input
    input_data = convert_pabutools_input(instance, profile)
    
    # Initialize tracker if analytics enabled
    tracker = RoundTracker(input_data.budget) if analytics else None
    
    # Create tracking callback
    def track_round(project_id: int, cost: float, 
                   effective_votes: Dict[int, float],
                   voter_budgets: Dict[int, float]) -> None:
        if tracker:
            tracker.add_round(
                selected_project=project_id,
                effective_votes=effective_votes,
                voter_budgets=voter_budgets
            )
            tracker.update_budget(cost)
            
    # Run algorithm
    winners, _ = equal_shares(
        voters=input_data.voters,
        projects_costs=input_data.projects_costs,
        budget=input_data.budget,
        bids=input_data.bids,
        tracker_callback=track_round if analytics else None
    )

    if analytics and tracker:
        # Create MES details with iterations
        details = MESAllocationDetails([1] * len(input_data.voters))
        for round_info in tracker.rounds:
            iteration = create_mes_iteration(round_info, winners, instance, profile)
            details.iterations.append(iteration)
        
        # Create allocation with details
        allocation = BudgetAllocation()
        allocation.details = details
        
        # Add selected projects
        for project_id, cost in winners.items():
            if cost > 0:
                project = next(p for p in instance if int(p.name) == project_id)
                allocation.append(project)
                
        return allocation
    else:
        # Return simple budget allocation without analytics
        allocation = BudgetAllocation()
        for project_id, cost in winners.items():
            if cost > 0:
                project = next(p for p in instance if int(p.name) == project_id)
                allocation.append(project)
        return allocation
