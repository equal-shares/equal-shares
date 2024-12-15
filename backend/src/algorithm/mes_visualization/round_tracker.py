"""
Tracks and records information about each round of the Equal Shares algorithm execution.
This module provides classes to collect and store data needed for visualization.

Key classes:
    - RoundInfo: Stores data about a single algorithm round
    - RoundTracker: Manages collection of rounds and current execution state
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import copy
import logging

logger = logging.getLogger(__name__)

@dataclass
class RoundInfo:
    """
    Stores comprehensive information about a single round of the algorithm.
    
    Attributes:
        round_number: Sequential number of this round (1-based)
        selected_project: ID of project selected in this round
        effective_votes: Maps project IDs to their effective vote counts
        voter_budgets: Maps voter IDs to their remaining budgets
        remaining_budget: Total budget remaining after this round
        dropped_projects: List of projects that became ineligible
    """
    # Required field - round must have a number
    round_number: int
    
    # Optional fields with default values
    selected_project: Optional[Any] = None  # Usually an int ID
    effective_votes: Dict[int, float] = field(default_factory=dict)
    voter_budgets: Dict[int, float] = field(default_factory=dict)
    remaining_budget: float = 0
    dropped_projects: List[Any] = field(default_factory=list)
    
    def snapshot_voter_budgets(self, current_budgets: Dict[int, float]) -> None:
        """
        Creates a deep copy (ensure budget changes don't affect historical data)
        of current voter budgets to avoid reference issues.
        
        Args:
            current_budgets: Dictionary mapping voter IDs to their current budgets
        """
        self.voter_budgets = copy.deepcopy(current_budgets)
        logger.debug(
            f"Round {self.round_number}: Snapshot of {len(current_budgets)} voter budgets taken"
        )

class RoundTracker:
    """
    Manages tracking of algorithm execution rounds for visualization purposes.
    
    This class maintains an ordered list of rounds and provides methods to:
    - Start new rounds
    - Update round information
    - Track budget changes
    - Record project selections
    
    Attributes:
        rounds: List of RoundInfo objects in execution order
        current_round: Number of current round (0 if not started)
        initial_budget: Starting budget value
        remaining_budget: Current remaining budget
    """
    
    def __init__(self, initial_budget: float):
        """
        Initialize a new round tracker.
        
        Args:
            initial_budget: Total budget at start of algorithm
        """
        self.rounds: List[RoundInfo] = []
        self.current_round = 0
        self.initial_budget = initial_budget
        self.remaining_budget = initial_budget
        logger.info(f"RoundTracker initialized with budget {initial_budget}")

    def start_round(self) -> RoundInfo:
        """
        Start a new round and return its info object.
        
        Returns:
            RoundInfo object for the new round
            
        Note:
            Automatically increments round number and sets remaining budget
        """
        self.current_round += 1
        round_info = RoundInfo(
            round_number=self.current_round,
            remaining_budget=self.remaining_budget
        )
        self.rounds.append(round_info)
        logger.debug(f"Started round {self.current_round}")
        return round_info

    def update_current_round(self, 
                           selected_project: Any = None,
                           effective_votes: Dict[int, float] = None,
                           voter_budgets: Dict[int, float] = None,
                           dropped_projects: List[Any] = None) -> None:
        """
        Update information for the current round.
        
        Args:
            selected_project: ID of project chosen this round
            effective_votes: Current effective vote counts per project
            voter_budgets: Current budget remaining per voter
            dropped_projects: Projects that became ineligible
            
        Raises:
            ValueError: If no round is active (start_round not called)
            
        Note:
            Only updates provided values, keeps existing values for others
        """
        if not self.rounds:
            raise ValueError("No active round - call start_round() first")
            
        current = self.rounds[-1]
        
        if selected_project is not None:
            current.selected_project = selected_project
            logger.debug(f"Round {self.current_round}: Selected project {selected_project}")
            
        if effective_votes is not None:
            current.effective_votes.update(effective_votes)
            logger.debug(
                f"Round {self.current_round}: Updated effective votes for "
                f"{len(effective_votes)} projects"
            )
            
        if voter_budgets is not None:
            current.snapshot_voter_budgets(voter_budgets)
            
        if dropped_projects is not None:
            current.dropped_projects.extend(dropped_projects)
            logger.debug(
                f"Round {self.current_round}: Added {len(dropped_projects)} "
                "dropped projects"
            )

    def project_selected(self, project_id: int, cost: float) -> None:
        """
        Record project selection and update remaining budget.
        
        Args:
            project_id: ID of selected project
            cost: Cost of selected project
        """
        self.remaining_budget -= cost
        self.update_current_round(selected_project=project_id)
        logger.info(
            f"Round {self.current_round}: Selected project {project_id} "
            f"(cost: {cost}, remaining: {self.remaining_budget})"
        )
