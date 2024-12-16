"""Wrapper for collecting visualization data during algorithm execution"""
from typing import Tuple, Dict, List, Any
from src.algorithm.equal_shares import equal_shares
from src.logger import get_logger
from .round_tracker import RoundTracker
from .pabutools_adapter import CustomBudgetAllocation

logger = get_logger()

def track_algorithm_round(
    tracker: RoundTracker,
    project_id: int, 
    effective_votes: Dict[int, float],
    voter_budgets: Dict[int, float],
    cost: float
) -> None:
    """Record single round of execution for visualization"""
    tracker.update_budget(cost)
    tracker.add_round(
        selected_project=project_id,
        effective_votes=effective_votes,
        voter_budgets=voter_budgets
    )

def run_algorithm_with_tracking(
    voters: List[int],
    projects_costs: Dict[int, int],
    budget: float,
    bids: Dict[int, Dict[int, int]]
) -> Tuple[Dict[int, int], RoundTracker]:
    """Run algorithm while collecting visualization data"""
    logger.info("Running algorithm with visualization tracking")
    tracker = RoundTracker(budget)
    
    winners = equal_shares(
        voters=voters,
        projects_costs=projects_costs,
        budget=budget,
        bids=bids,
        round_callback=lambda pid, votes, budgets, cost: track_algorithm_round(
            tracker, pid, votes, budgets, cost
        )
    )
    
    logger.info(f"Algorithm completed: {len(winners)} winners in {len(tracker.rounds)} rounds")
    return winners, tracker

def create_visualization_output(
    winners: Dict[int, int],
    tracker: RoundTracker,
    projects_meta: Dict[int, Any]
) -> CustomBudgetAllocation:
    """Convert algorithm results to pabutools format"""
    from .pabutools_adapter import CustomBudgetAllocation
    return CustomBudgetAllocation(
        selected_projects=winners,
        round_tracker=tracker,
        projects_meta=projects_meta
    )
