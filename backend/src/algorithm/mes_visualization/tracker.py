from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class RoundInfo:
    """Information about a single round of the MES algorithm."""
    selected_project: int
    cost: float
    effective_votes: Dict[int, float]
    voter_budgets: Dict[int, float]
    is_budget_update: bool = False

    def __str__(self) -> str:
        return (f"Round(project={self.selected_project}, "
                f"cost={self.cost}, votes={len(self.effective_votes)})")

class MESTracker:
    """Tracks rounds of the MES algorithm for visualization."""
    
    def __init__(self):
        self.rounds: list[RoundInfo] = []
        
    def __call__(self, 
                 project_id: int, 
                 cost: float, 
                 effective_votes: Dict[int, float],
                 voter_budgets: Dict[int, float]) -> None:
        """Callback function for the MES algorithm to track rounds.
        
        Args:
            project_id: ID of the selected project
            cost: Cost allocated to the project
            effective_votes: Dict mapping project IDs to their effective votes
            voter_budgets: Dict mapping voter IDs to their remaining budgets
        """
        self.rounds.append(RoundInfo(
            selected_project=project_id,
            cost=cost,
            effective_votes=effective_votes,  # Using project IDs as keys
            voter_budgets=voter_budgets.copy(),  # Make a copy to prevent reference issues
            is_budget_update=cost == 0
        ))
    
    def __len__(self) -> int:
        return len(self.rounds)
