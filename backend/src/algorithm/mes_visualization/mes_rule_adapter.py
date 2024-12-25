"""Custom implementation of Method of Equal Shares (MES) that bridges 
pabutools interface with our implementation."""

from typing import Optional, Dict, List, Any
from dataclasses import dataclass
from gmpy2 import mpq

from pabutools.election import Instance, AbstractProfile, Cost_Sat, Project
from pabutools.rules import BudgetAllocation
from pabutools.rules.mes.mes_details import MESAllocationDetails, MESIteration, MESProjectDetails

from src.algorithm.equal_shares import equal_shares
from src.algorithm.mes_visualization.tracker import RoundInfo, MESTracker

@dataclass
class MESInput:
    """Normalized input data for MES algorithm."""
    voters: List[int]
    projects_costs: Dict[int, int]
    budget: float
    bids: Dict[int, Dict[int, int]]
    projects_meta: Dict[int, Any]

def create_mes_iteration(round_info: RoundInfo, instance: Instance, profile: AbstractProfile) -> Optional[MESIteration]:
    """Create MES iteration details for visualization."""
    if round_info.is_budget_update or round_info.cost == 0:
        return None

    iteration = MESIteration()
    
    try:
        # Create map of project names to the ORIGINAL pabutools Project instances
        project_map = {p.name: p for p in instance}
        # print(f'project_map: {project_map}')
        
        # Set supporter indices using original instances
        for proj in instance:  # Use pabutools' instances directly
            # print(f'- proj: {proj}')
            vote_indices = [i for i, ballot in enumerate(profile) if proj in ballot]
            proj.supporter_indices = vote_indices
            # print(f'proj.supporter_indices: {proj.supporter_indices}')
        
        # Create effective votes mapping using original Project instances
        effective_votes_map = {}
        for proj_id, votes in round_info.effective_votes.items():
            # print(f'proj_id: votes - {proj_id}: {votes}')
            proj = project_map[str(proj_id)]  # Use string name to lookup original instance
            effective_votes_map[proj] = votes
            proj.effective_vote_count = votes
            proj.affordability = 1.0 / votes if votes > 0 else float('inf') # Higher votes = lower affordability
            
            proj_details = MESProjectDetails(proj, iteration)
            proj_details.affordability = proj.affordability
            proj_details.effective_vote_count = votes
            iteration.append(proj_details)
        # print(f'effective_votes_map: {effective_votes_map}')

        # Set selected project using original instance
        selected_proj = project_map[str(round_info.selected_project)]
        iteration.selected_project = selected_proj
        
        # Set iteration properties
        iteration.effective_vote_count = effective_votes_map
        # print(f'iteration.effective_vote_count: {effective_votes_map}')
        # TODO: voters_budget and voters_budget_after_selection get the same value, have to fix that?
        iteration.voters_budget = list(round_info.voter_budgets.values())
        # print(f'iteration.voters_budget: {list(round_info.voter_budgets.values())}')
        iteration.voters_budget_after_selection = list(round_info.voter_budgets.values())
        # print(f'iteration.voters_budget_after_selection: {list(round_info.voter_budgets.values())}')

        # Debug verification with memory addresses
        print(f"\nIteration details:")
        print(f"  Selected project: {id(iteration.selected_project)}")
        for proj, votes in effective_votes_map.items():
            print(f"  Project {proj.name}: id={id(proj)}, votes={votes}")

        print(f'- returned iteration: {iteration}')

        return iteration
        
    except Exception as e:
        print(f"Error in create_mes_iteration: {str(e)}")
        raise

def convert_pabutools_input(instance: Instance, profile: AbstractProfile) -> MESInput:
    """Convert pabutools input format to algorithm format."""
    # Extract voters
    voters = list(range(len(profile)))
    
    # Extract project costs
    projects_costs = {
        int(project.name): meta.get('min_points', float(project.cost))
        for project in instance
        for meta in [instance.project_meta.get(str(project.name), {})]
    }
    
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
        # Fallback to binary approval
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

def method_of_equal_shares(
    instance: Instance,
    profile: AbstractProfile,
    sat_class: Optional[type] = None,
    analytics: bool = False,
    verbose: bool = False,
    **kwargs
) -> BudgetAllocation:
    """Run MES algorithm and create visualization data."""
    # Convert input
    input_data = convert_pabutools_input(instance, profile)
    
    # Create tracker to collect round information
    tracker = MESTracker()
    print("\nDEBUG - Created tracker")

    # Run algorithm and get final winners
    print("DEBUG - About to run equal_shares with tracker")
    winners, payments = equal_shares(
        voters=input_data.voters,
        projects_costs=input_data.projects_costs,
        budget=input_data.budget,
        bids=input_data.bids,
        tracker_callback=tracker
    )

    print(f"DEBUG - Winners and their allocations: {winners}")
    print(f"DEBUG - Total rounds tracked: {len(tracker)}")

    # Create allocation with the allocated amounts
    allocation = BudgetAllocation()
    
    if analytics:
        details = MESAllocationDetails([1] * len(input_data.voters))
        
        # Create iterations from tracker rounds
        project_iterations = []
        for round_info in tracker.rounds:
            print(f'round_info: {round_info}')
            iteration = create_mes_iteration(round_info, instance, profile)
            if iteration is not None:
                project_iterations.append(iteration)
                # print(f"Added iteration for project {round_info.selected_project}")
        
        print(f'- details: {details}')

        details.iterations = project_iterations
        details.allocations = winners
        allocation.details = details
        
        print(f"DEBUG - Created {len(project_iterations)} iterations for visualization")
    
    # Add winning projects to allocation
    for project_id, allocated_cost in winners.items():
        if allocated_cost > 0:
            project = next(p for p in instance if int(p.name) == project_id)
            project.cost = mpq(str(allocated_cost))
            allocation.append(project)

    return allocation
