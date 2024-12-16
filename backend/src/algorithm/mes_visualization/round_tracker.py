"""Basic tracking for equal shares algorithm execution"""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from src.logger import get_logger, LoggerName

logger = get_logger(LoggerName.ALGORITHM)

@dataclass
class RoundInfo:
    """Data for single algorithm round"""
    selected_project: Optional[int] = None
    # Maps project IDs to their effective vote counts (support strength)
    effective_votes: Dict[int, float] = field(default_factory=dict)
    voter_budgets: Dict[int, float] = field(default_factory=dict)
    remaining_budget: float = 0  # Budget after selection
    dropped_projects: List[int] = field(default_factory=list)

class RoundTracker:
    """Collects data during algorithm execution for visualization"""
    def __init__(self, initial_budget: float):
        self.rounds: List[RoundInfo] = []
        self.initial_budget = initial_budget
        self.remaining_budget = initial_budget
        logger.info(f"Starting tracking with budget {initial_budget}")

    def add_round(self, 
                 selected_project: Optional[int] = None,
                 effective_votes: Optional[Dict[int, float]] = None,
                 voter_budgets: Optional[Dict[int, float]] = None,
                 dropped_projects: Optional[List[int]] = None) -> RoundInfo:
        """Record data for new round"""
        # Create round with provided data
        round_info = RoundInfo(
            selected_project=selected_project,
            remaining_budget=self.remaining_budget
        )
        
        if effective_votes:
            round_info.effective_votes = effective_votes.copy()
        if voter_budgets:
            round_info.voter_budgets = voter_budgets.copy()
        if dropped_projects:
            round_info.dropped_projects = dropped_projects.copy()
            
        self.rounds.append(round_info)
        logger.debug(f"Round {len(self.rounds)}: Selected project {selected_project}")
        return round_info

    def update_budget(self, cost: float) -> None:
        """Update budget after project selection"""
        self.remaining_budget -= cost
        logger.debug(f"Budget updated: -{cost} = {self.remaining_budget}")
