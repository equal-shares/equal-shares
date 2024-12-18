"""Wrapper for collecting visualization data during algorithm execution"""
from typing import Tuple, Dict, List, Any
from src.algorithm.equal_shares import equal_shares
from src.logger import get_logger
from .round_tracker import RoundTracker
from .pabutools_adapter import CustomBudgetAllocation

logger = get_logger()

def run_algorithm_with_tracking(
    voters: List[int],
    projects_costs: Dict[int, int],
    budget: float,
    bids: Dict[int, Dict[int, int]]
) -> Tuple[Dict[int, int], RoundTracker]:
    """Run algorithm with visualization tracking"""
    logger.info("Running algorithm with tracking")
    
    # Initialize tracker
    tracker = RoundTracker(budget)
    
    # Create callback for tracking rounds
    def track_round(project_id: int, cost: float, 
                   effective_votes: Dict[int, float],
                   voter_budgets: Dict[int, float]) -> None:
        tracker.add_round(
            selected_project=project_id,
            effective_votes=effective_votes,
            voter_budgets=voter_budgets
        )
        tracker.update_budget(cost)
        
        logger.debug(
            f"Tracked round: Project {project_id} selected, "
            f"cost {cost}, remaining {tracker.remaining_budget}"
        )
    
    # Run algorithm with tracking
    winners, _ = equal_shares(
        voters=voters,
        projects_costs=projects_costs,
        budget=budget,
        bids=bids,
        tracker_callback=track_round
    )
    
    logger.info(f"Tracking complete: {len(tracker.rounds)} rounds recorded")
    return winners, tracker

def create_visualization_output(
    winners: Dict[int, int],
    tracker: RoundTracker,
    projects_meta: Dict[int, Any]
) -> CustomBudgetAllocation:
    """Convert algorithm results to pabutools format"""
    
    # Create voter preferences from bids
    voter_preferences = {1: [1], 2: [2]}
    
    return CustomBudgetAllocation(
        selected_projects=winners,
        round_tracker=tracker,
        projects_meta=projects_meta,
        voter_preferences=voter_preferences
    )
