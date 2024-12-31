from dataclasses import dataclass
from typing import Dict, Optional
from src.logger import get_logger, LoggerName

logger = get_logger(LoggerName.ALGORITHM)

@dataclass
class RoundInfo:
    """Information about a single round of the MES algorithm."""
    selected_project: int
    cost: float
    effective_votes: Dict[str, float]
    voter_budgets: Dict[int, float]
    previous_allocations: Dict[int, float]  # Budget states before this round
    payments_per_voter: Dict[int, float]    # What each voter paid this round

    def __str__(self) -> str:
        return (f"Round(project={self.selected_project}, "
                f"cost={self.cost}, votes={len(self.effective_votes)})")

class MESTracker:
    """Tracks rounds of the MES algorithm for visualization."""
    
    def __init__(self):
        self.rounds: list[RoundInfo] = []
        self.total_allocations: Dict[int, float] = {}
        self.current_voter_budgets: Dict[int, float] = {}
        self.previous_allocations: Dict[int, float] = {}  # Track previous state
        # logger.debug("Initialized MESTracker")

    def __call__(self, 
                 project_id: int, 
                 cost: float, 
                 effective_votes: Dict[str, float],
                 voter_budgets: Dict[int, float],
                 payments_per_voter: Dict[int, float],
                 previous_allocations: Optional[Dict[int, float]] = None) -> None:
        """Callback function for the MES algorithm to track rounds.
        
        Args:
            project_id: ID of the selected project
            cost: Cost allocated to the project
            effective_votes: Dict mapping project IDs to their effective votes
            voter_budgets: Dict mapping voter IDs to their remaining budgets
            payments_per_voter: Dict mapping voter IDs to their payments for this project
            previous_allocations: Optional dict of voter budgets before this round
        """
        # logger.debug(f"MESTracker receiving round:")
        # logger.debug(f"Project ID: {project_id}")
        # logger.debug(f"Cost: {cost}")
        # logger.debug(f"Effective votes: {effective_votes}")
        # logger.debug(f"Payments per voter: {payments_per_voter}")
        # logger.debug(f"Current rounds count: {len(self.rounds)}")

        # Update total allocations
        if project_id not in self.total_allocations:
            self.total_allocations[project_id] = 0
        self.total_allocations[project_id] = cost

        # Update current voter budgets
        self.current_voter_budgets = voter_budgets.copy()
        
        # Use provided previous allocations or current tracked state
        if previous_allocations is None:
            previous_allocations = self.previous_allocations.copy()
        
        # Create round info
        round_info = RoundInfo(
            selected_project=project_id,
            cost=cost,
            effective_votes=effective_votes,
            voter_budgets=self.current_voter_budgets.copy(),
            previous_allocations=previous_allocations,
            payments_per_voter=payments_per_voter
        )
        
        self.rounds.append(round_info)
        
        # Update previous allocations for next round
        self.previous_allocations = voter_budgets.copy()
        
        # logger.debug(f"Total rounds after append: {len(self.rounds)}")
    
    def __len__(self) -> int:
        return len(self.rounds)
