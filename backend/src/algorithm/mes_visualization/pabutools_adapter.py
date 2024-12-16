"""Adapts algorithm output to pabutools visualization format"""
from dataclasses import dataclass
from typing import Dict, List, Any
from pabutools.rules import BudgetAllocation
from .round_tracker import RoundTracker

@dataclass
class ProjectDetails:
    project: Any 
    name: str
    cost: float
    supporter_indices: List[int]
    affordability: float

class CustomBudgetAllocation(BudgetAllocation):
    def __init__(self, 
                selected_projects: Dict[int, float],
                round_tracker: RoundTracker,
                projects_meta: Dict[int, Any],
                voter_preferences: Dict[int, List[int]]):
        """
        Args:
            selected_projects: Maps project IDs to their costs
            round_tracker: Round-by-round execution data
            projects_meta: Project metadata
            voter_preferences: Maps voter IDs to their supported project IDs
        """
        super().__init__()
        self._selected = selected_projects
        self.details = self._create_details(
            round_tracker, 
            projects_meta,
            voter_preferences
        )

    def __contains__(self, project) -> bool:
        """Check if project was selected"""
        return (project.name in self._selected and 
                self._selected[int(project.name)] > 0)

    def _create_details(self, tracker, projects_meta, 
                       voter_preferences) -> Any:
        """Create visualization data using correct voter preferences"""
        class Details:
            def __init__(self, iterations):
                self.iterations = iterations

        iterations = []
        selected_projects = set()
        
        for round_info in tracker.rounds:
            project_id = round_info.selected_project
            project = projects_meta[project_id]
            
            # Get actual supporters based on preferences
            supporters = [
                voter_id for voter_id, preferred_projects 
                in voter_preferences.items()
                if project_id in preferred_projects
            ]

            # Create project details
            project_details = ProjectDetails(
                project=project,
                name=str(project_id),
                cost=project.min_points,
                supporter_indices=supporters,
                affordability=1/round_info.effective_votes.get(project_id, 1)
            )
            
            # Track selected project
            selected_projects.add(project_id)
            
            # Create iteration
            iteration = type('IterationDetails', (), {
                'voters_budget': round_info.voter_budgets,
                'voters_budget_after_selection': round_info.voter_budgets,
                'selected_project': project_details,
                'get_all_projects': lambda: [
                    ProjectDetails(
                        project=projects_meta[pid],
                        name=str(pid),
                        cost=projects_meta[pid].min_points,
                        supporter_indices=[
                            vid for vid, prefs in voter_preferences.items()
                            if pid in prefs
                        ],
                        affordability=1/votes,
                        discarded=pid in selected_projects
                    )
                    for pid, votes in round_info.effective_votes.items()
                ]
            })
            
            iterations.append(iteration)

        return Details(iterations)
