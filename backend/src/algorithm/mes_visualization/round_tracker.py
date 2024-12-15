from dataclasses import dataclass, field
from typing import Dict, List, Any
import copy

@dataclass
class RoundInfo:
    """Stores information about a single round of the algorithm"""
    round_number: int
    selected_project: Any = None
    effective_votes: Dict[int, float] = field(default_factory=dict)
    voter_budgets: Dict[int, float] = field(default_factory=dict)
    remaining_budget: float = 0
    dropped_projects: List[Any] = field(default_factory=list)
    
    def snapshot_voter_budgets(self, current_budgets: Dict[int, float]):
        """Create a deep copy of current voter budgets"""
        self.voter_budgets = copy.deepcopy(current_budgets)

class RoundTracker:
    """Tracks algorithm execution rounds for visualization"""
    def __init__(self, initial_budget: float):
        self.rounds: List[RoundInfo] = []
        self.current_round = 0
        self.initial_budget = initial_budget
        self.remaining_budget = initial_budget

    def start_round(self) -> RoundInfo:
        """Start a new round and return its info object"""
        self.current_round += 1
        round_info = RoundInfo(
            round_number=self.current_round,
            remaining_budget=self.remaining_budget
        )
        self.rounds.append(round_info)
        return round_info

    def update_current_round(self, 
                           selected_project: Any = None,
                           effective_votes: Dict[int, float] = None,
                           voter_budgets: Dict[int, float] = None,
                           dropped_projects: List[Any] = None):
        """Update current round with new information"""
        if not self.rounds:
            raise ValueError("No active round - call start_round() first")
            
        current = self.rounds[-1]
        
        if selected_project is not None:
            current.selected_project = selected_project
            
        if effective_votes is not None:
            current.effective_votes.update(effective_votes)
            
        if voter_budgets is not None:
            current.snapshot_voter_budgets(voter_budgets)
            
        if dropped_projects is not None:
            current.dropped_projects.extend(dropped_projects)

    def project_selected(self, project_id: int, cost: float):
        """Record project selection and update budget"""
        self.remaining_budget -= cost
        self.update_current_round(selected_project=project_id)
