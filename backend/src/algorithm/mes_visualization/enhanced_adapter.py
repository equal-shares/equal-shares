"""
Enhanced adapter for MES visualization that properly handles multi-pass allocations.
"""
from typing import Any

from dataclasses import dataclass
from typing import Dict, List, Optional
from pabutools.rules import BudgetAllocation
from pabutools.election import Instance, Project
from pabutools.rules.mes.mes_details import MESAllocationDetails, MESIteration, MESProjectDetails

@dataclass
class FinalAllocation:
    """Represents the final state of a project allocation after all iterations."""
    project_id: int
    final_cost: float
    effective_votes: float
    supporter_indices: List[int]

class EnhancedRoundTracker:
    """Tracks both interim and final allocation states."""
    def __init__(self, initial_budget: float):
        self.initial_budget = initial_budget
        self.remaining_budget = initial_budget
        self.final_allocations: Dict[int, FinalAllocation] = {}
        self._current_round_data = {}
        
    def update_round(self, 
                    selected_project: int,
                    cost: float,
                    effective_votes: Dict[int, float],
                    voter_indices: List[int]) -> None:
        """Track latest round data for a project."""
        if selected_project not in self.final_allocations:
            self.final_allocations[selected_project] = FinalAllocation(
                project_id=selected_project,
                final_cost=cost,
                effective_votes=effective_votes.get(selected_project, 0),
                supporter_indices=voter_indices
            )
        else:
            # Update existing allocation
            current = self.final_allocations[selected_project]
            current.final_cost = cost
            current.effective_votes = effective_votes.get(selected_project, 0)
            current.supporter_indices = voter_indices
            
        self.remaining_budget -= cost

def create_visualization_details(
    instance: Instance,
    tracker: EnhancedRoundTracker,
    profile: Any  # Type hint as Any to avoid circular imports
) -> MESAllocationDetails:
    """Create visualization details from final allocations."""
    
    # Initialize details with voter budgets
    details = MESAllocationDetails([tracker.initial_budget / len(profile)] * len(profile))
    
    # Create iterations only for final allocations
    iterations = []
    
    for project_id, allocation in tracker.final_allocations.items():
        # Find corresponding project in instance
        project = next(p for p in instance if int(p.name) == project_id)
        
        # Create iteration for this project
        iteration = MESIteration()
        iteration.effective_vote_count = {}  # Initialize the dictionary
        
        # Set project properties for selected project
        project.supporter_indices = allocation.supporter_indices
        project.affordability = 1.0 / allocation.effective_votes if allocation.effective_votes > 0 else float('inf')
        project.effective_vote_count = allocation.effective_votes
        
        # Create project details for selected project
        project_details = MESProjectDetails(project, iteration)
        project_details.affordability = project.affordability
        project_details.effective_vote_count = project.effective_vote_count
        
        # Add selected project to iteration
        iteration.selected_project = project
        iteration.append(project_details)
        iteration.effective_vote_count[project] = project.effective_vote_count
        
        # Add details for all other projects
        for other_proj in instance:
            if int(other_proj.name) != project_id:
                # Calculate supporter indices
                other_voter_indices = []
                for voter_idx, ballot in enumerate(profile):
                    if other_proj in ballot:
                        other_voter_indices.append(voter_idx)
                
                # Set properties for other project
                other_proj.supporter_indices = other_voter_indices
                # Default to 0 effective votes for unselected projects
                other_proj.effective_vote_count = 0
                other_proj.affordability = float('inf')
                
                # Create and add details
                other_details = MESProjectDetails(other_proj, iteration)
                other_details.affordability = other_proj.affordability
                other_details.effective_vote_count = other_proj.effective_vote_count
                iteration.append(other_details)
                iteration.effective_vote_count[other_proj] = other_proj.effective_vote_count
        
        # Set budget information
        budget_per_voter = tracker.initial_budget / len(profile)
        iteration.voters_budget = [budget_per_voter] * len(profile)
        iteration.voters_budget_after_selection = [
            budget_per_voter if i not in allocation.supporter_indices 
            else max(0, budget_per_voter - (allocation.final_cost / len(allocation.supporter_indices)))
            for i in range(len(profile))
        ]
        
        iterations.append(iteration)
    
    details.iterations = iterations
    return details

def create_mes_outcome(
    instance: Instance,
    tracker: EnhancedRoundTracker,
    profile: Any
) -> BudgetAllocation:
    """Create final budget allocation with visualization details."""
    
    # Create allocation object
    allocation = BudgetAllocation()
    
    # Add visualization details
    allocation.details = create_visualization_details(instance, tracker, profile)
    
    # Add only projects with final allocations
    for project_id, alloc in tracker.final_allocations.items():
        if alloc.final_cost > 0:
            project = next(p for p in instance if int(p.name) == project_id)
            allocation.append(project)
    
    return allocation
