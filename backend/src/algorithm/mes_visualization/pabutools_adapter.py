from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from pabutools.rules import BudgetAllocation
from .round_tracker import RoundTracker

@dataclass
class ProjectDetails:
    """
    Adapts our project data to match pabutools' expected format.
    
    This class mimics pabutools' internal project representation, providing
    the same interface that the visualization expects.
    
    Attributes:
        project: Original project object from our system
        project_id: Unique identifier for the project
        cost: Project's cost/price
        supporter_indices: List of voter IDs who supported this project
        affordability: Inverse of effective vote count (1/votes)
        discarded: Whether project was dropped from consideration
    """
    project: Any
    project_id: int
    cost: float
    supporter_indices: List[int]
    affordability: float  
    discarded: bool = False
    
    def __str__(self) -> str:
        """String representation matching pabutools format"""
        return f"Project({self.project_id}, cost={self.cost})"
    
    @property
    def name(self) -> str:
        """Property required by pabutools visualizer"""
        return str(self.project_id)

@dataclass
class IterationDetails:
    """
    Represents one round/iteration of the algorithm execution.
    
    Stores the state of voter budgets before and after a project selection,
    matching pabutools' iteration data structure.
    
    Attributes:
        voters_budget: Dict mapping voter IDs to their budgets at start of round
        voters_budget_after_selection: Budgets after project selection
        selected_project: ProjectDetails of chosen project (if any)
        _all_projects: Cache of all projects in this round
    """
    voters_budget: Dict[int, float]
    voters_budget_after_selection: Dict[int, float]
    selected_project: Optional[ProjectDetails] = None
    _all_projects: List[ProjectDetails] = field(default_factory=list)

    def get_all_projects(self) -> List[ProjectDetails]:
        """
        Returns all projects available in this iteration.
        
        Required by pabutools visualizer to show project status per round.
        """
        return self._all_projects

    def add_project(self, project: ProjectDetails) -> None:
        """Add a project to this iteration's tracking"""
        self._all_projects.append(project)

class CustomAllocationDetails:
    """
    Converts our round-by-round data into pabutools' expected format.
    
    This adapter transforms our RoundTracker data into a sequence of
    IterationDetails that match pabutools' visualization requirements.
    
    Attributes:
        iterations: List of IterationDetails representing algorithm execution
    """
    def __init__(self, round_tracker: 'RoundTracker', projects_meta: Dict):
        """
        Initialize from our tracking data.
        
        Args:
            round_tracker: Our round-by-round execution data
            projects_meta: Original project information
        """
        self.iterations = self._convert_rounds(round_tracker, projects_meta)
        
    def _convert_rounds(
        self, 
        tracker: 'RoundTracker', 
        projects_meta: Dict
    ) -> List[IterationDetails]:
        """
        Convert our round data to pabutools iteration format.
        
        This is the core conversion logic that transforms our tracking
        format into the structure expected by pabutools visualization.
        
        Args:
            tracker: RoundTracker containing our execution data
            projects_meta: Dictionary of project metadata
            
        Returns:
            List of IterationDetails matching pabutools format
        """
        iterations = []
        previous_budgets = None
        
        # Process each round of our execution
        for round_info in tracker.rounds:
            # Create iteration with budget snapshots
            iteration = IterationDetails(
                voters_budget=round_info.voter_budgets,
                # Use previous round's budgets or current if first round
                voters_budget_after_selection=(
                    previous_budgets if previous_budgets 
                    else round_info.voter_budgets
                )
            )
            
            # Convert selected project if any
            if round_info.selected_project is not None:
                project_id = round_info.selected_project
                project_meta = projects_meta[project_id]
                
                # Create pabutools-compatible project details
                iteration.selected_project = ProjectDetails(
                    project=project_meta,
                    project_id=project_id,
                    cost=project_meta.min_points,  # Use min cost as base
                    # Get voters with remaining budget
                    supporter_indices=[
                        vid for vid, budget 
                        in round_info.voter_budgets.items() 
                        if budget > 0
                    ],
                    # Calculate affordability from effective votes
                    affordability=1/round_info.effective_votes.get(
                        project_id, 1
                    )
                )
                
            # Track available projects (both selected and dropped)
            for proj_id, votes in round_info.effective_votes.items():
                project_meta = projects_meta[proj_id]
                iteration.add_project(ProjectDetails(
                    project=project_meta,
                    project_id=proj_id,
                    cost=project_meta.min_points,
                    supporter_indices=[
                        vid for vid, budget 
                        in round_info.voter_budgets.items() 
                        if budget > 0
                    ],
                    affordability=1/votes,
                    discarded=proj_id in round_info.dropped_projects
                ))
            
            iterations.append(iteration)
            previous_budgets = round_info.voter_budgets
            
        return iterations

class CustomBudgetAllocation(BudgetAllocation):
    """
    Top-level adapter implementing pabutools' BudgetAllocation interface.
    
    This class makes our algorithm results compatible with pabutools'
    visualization by implementing the expected interface.
    
    Attributes:
        _selected: Dict mapping project IDs to their allocations
        details: CustomAllocationDetails containing round information
    """
    def __init__(
        self, 
        selected_projects: Dict[int, float],
        round_tracker: 'RoundTracker',
        projects_meta: Dict
    ):
        """
        Initialize budget allocation adapter.
        
        Args:
            selected_projects: Dict of project allocations
            round_tracker: Round-by-round execution data
            projects_meta: Original project information
        """
        super().__init__()
        self._selected = selected_projects
        self.details = CustomAllocationDetails(round_tracker, projects_meta)
        
    def __contains__(self, project) -> bool:
        """
        Test if a project was selected.
        
        Required by pabutools to determine which projects were chosen.
        
        Args:
            project: Project to test (in pabutools format)
            
        Returns:
            bool: True if project was selected with non-zero allocation
        """
        return (project.name in self._selected and 
                self._selected[project.name] > 0)
                
    def get_allocation(self) -> Dict[str, float]:
        """
        Get final project allocations.
        
        Returns allocations in pabutools' expected format with string IDs.
        
        Returns:
            Dict mapping project IDs (as strings) to allocated amounts
        """
        return {str(k): v for k, v in self._selected.items()}
