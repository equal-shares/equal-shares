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
from src.logger import get_logger, LoggerName

logger = get_logger(LoggerName.ALGORITHM)

@dataclass
class MESInput:
    """Normalized input data for MES algorithm."""
    voters: List[int]
    projects_costs: Dict[int, int]
    budget: float
    bids: Dict[int, Dict[int, int]]
    projects_meta: Dict[int, Any]

def create_mes_iteration(round_info: RoundInfo, instance: Instance, profile: AbstractProfile) -> Optional[MESIteration]:
    """
    Create MES iteration details for visualization.
    Maps data from our custom implementation to pabutools' expected format.

    Args:
        round_info: Single round information from our custom MES implementation
        instance: PabuTools instance containing project information
        profile: PabuTools profile containing voter preferences

    Returns:
        Optional[MESIteration]: Pabutools iteration object or None if round should be skipped
    """
    if round_info.is_budget_update:
        return None

    iteration = MESIteration()
    
    try:
        # Calculate correct budget information
        total_budget = float(instance.budget_limit)
        voters_count = len(profile)
        initial_voter_budget = total_budget / voters_count
        
        # Create map of project IDs to actual Project instances
        project_map = {p.name: p for p in instance}
        
        # Set supporter indices and project details for ALL projects
        for proj in instance:
            # Get original voter indices who supported this project
            vote_indices = [i for i, ballot in enumerate(profile) if proj in ballot]
            proj.supporter_indices = vote_indices

            # Create project details and add to iteration
            proj_details = MESProjectDetails(proj, iteration)
            iteration.append(proj_details)
            
            # Set effective votes and affordability for all projects
            proj_name = str(proj.name)  # Ensure string key
            effective_votes = round_info.effective_votes.get(proj_name, 0.0)
            
            # Apply to both Project and ProjectDetails objects
            for target in [proj, proj_details]:
                target.effective_vote_count = effective_votes
                target.affordability = 1.0 / effective_votes if effective_votes > 0 else float('inf')
                target.discarded = False  # Initialize as not discarded
            
            # Mark projects as discarded if they weren't selected in this round
            if int(proj.name) != round_info.selected_project:
                proj_details.discarded = True
        
        # Set the selected project for this round
        selected_proj = project_map[str(round_info.selected_project)]
        iteration.selected_project = selected_proj
        
        # Set budget information
        # Initial budgets (equal distribution)
        iteration.voters_budget = [initial_voter_budget for _ in range(voters_count)]
        
        # Remaining budgets after selection
        iteration.voters_budget_after_selection = []
        for voter_idx in range(voters_count):
            # Get remaining budget from round_info or use initial if not found
            remaining = round_info.voter_budgets.get(voter_idx + 1, initial_voter_budget)
            iteration.voters_budget_after_selection.append(remaining)

        # Debug logging
        logger.debug(f"\nIteration details for project {round_info.selected_project}:")
        logger.debug(f"  Selected project: {selected_proj.name}")
        logger.debug(f"  Initial voter budget: {initial_voter_budget}")
        logger.debug(f"  Total voters: {voters_count}")
        logger.debug("  Effective votes by project:")
        for proj in instance:
            logger.debug(f"    Project {proj.name}: "
                      f"votes={getattr(proj, 'effective_vote_count', 0)}, "
                      f"affordability={getattr(proj, 'affordability', 'N/A')}")

        return iteration
        
    except Exception as e:
        logger.error(f"Error creating MES iteration: {str(e)}")
        raise

def convert_pabutools_input(instance: Instance, profile: AbstractProfile) -> MESInput:
    """Convert pabutools input format to algorithm format."""
    # Extract voters
    voters = getattr(profile, '_voters', None)
    
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
    logger.debug("Created tracker")

    # Run algorithm and get final winners
    logger.debug("About to run equal_shares with tracker")
    winners, payments = equal_shares(
        voters=input_data.voters,
        projects_costs=input_data.projects_costs,
        budget=input_data.budget,
        bids=input_data.bids,
        tracker_callback=tracker
    )

    logger.debug(f"Winners and their allocations: {winners}")
    logger.debug(f"Total rounds tracked: {len(tracker)}")

    # Create allocation with the allocated amounts
    allocation = BudgetAllocation()
    
    if analytics:
        details = MESAllocationDetails([1] * len(input_data.voters))
        
        # Create iterations from tracker rounds
        project_iterations = []
        for round_info in tracker.rounds:
            logger.debug(f'round_info: {round_info}')
            iteration = create_mes_iteration(round_info, instance, profile)
            if iteration is not None:
                project_iterations.append(iteration)
        
        logger.debug(f'details: {details}')

        details.iterations = project_iterations
        details.allocations = winners
        allocation.details = details
        
        logger.debug(f"Created {len(project_iterations)} iterations for visualization")
    
    # Add winning projects to allocation
    for project_id, allocated_cost in winners.items():
        if allocated_cost > 0:
            project = next(p for p in instance if int(p.name) == project_id)
            project.cost = mpq(str(allocated_cost))
            allocation.append(project)

    return allocation
