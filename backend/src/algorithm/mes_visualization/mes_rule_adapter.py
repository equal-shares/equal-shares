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
    
    # Extract bids from profile
    bids = {}
    for project in instance:
        project_id = int(project.name)
        bids[project_id] = {}
        for voter_idx, ballot in enumerate(profile):
            # Convert approval ballot to bid
            if project in ballot:
                bids[project_id][voter_idx] = 1
            else:
                bids[project_id][voter_idx] = 0
                
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
    
    # Add required properties to Project object
    project_obj.supporter_indices = voter_indices  # Add supporter indices
    project_obj.affordability = 1.0 / round_info.effective_votes.get(round_info.selected_project, 1)
    
    # Create MESProjectDetails for the selected project
    project_details = MESProjectDetails(project_obj, iteration)
    project_details.affordability = project_obj.affordability
    
    # Set both the raw project and its details
    iteration.selected_project = project_obj
    iteration.append(project_details)
    
    # Add details for unselected projects
    for proj_id, votes in round_info.effective_votes.items():
        if proj_id != round_info.selected_project:
            other_proj = next(p for p in instance if int(p.name) == proj_id)
            
            # Calculate supporter indices for unselected project
            other_voter_indices = []
            for voter_idx, ballot in enumerate(profile):
                if other_proj in ballot:
                    other_voter_indices.append(voter_idx)
                    
            # Add properties to unselected Project
            other_proj.supporter_indices = other_voter_indices
            other_proj.affordability = 1.0 / votes
            
            # Create and add details
            other_details = MESProjectDetails(other_proj, iteration)
            other_details.affordability = other_proj.affordability
            iteration.append(other_details)
    
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
