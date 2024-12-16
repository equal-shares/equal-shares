"""Example showing how algorithm data is converted to pabutools format"""
from dataclasses import dataclass
from src.algorithm.mes_visualization.round_tracker import RoundTracker
from src.algorithm.mes_visualization.pabutools_adapter import CustomBudgetAllocation

@dataclass
class Project:
    project_id: int
    name: str
    min_points: int
    description: str

def run_adapter_example():
    """
    Scenario:
    - Total budget: 300
    - Initial per voter: 300/2 = 150 each
    - Voter 1 wants ONLY Library (100 points)
    - Voter 2 wants ONLY Park (150 points)
    """
    # Create test projects
    projects = {
        1: Project(1, "Library", 100, "Public library upgrade"),
        2: Project(2, "Park", 150, "Community park development")
    }
    
    # Create tracker with same scenario as round_tracker_example
    tracker = RoundTracker(300)
    
    # Track which voters support each project
    voter_preferences = {
        1: [1],    # Voter 1 supports only Library (project 1)
        2: [2]     # Voter 2 supports only Park (project 2)
    }
    
    # Round 1 - Library (100 points)
    tracker.add_round(
        selected_project=1,
        effective_votes={1: 1.0, 2: 0.0},  # Only Voter 1 supports Library
        voter_budgets={
            1: 50,   # Voter 1: 150 - 100 = 50
            2: 150   # Voter 2: Unchanged
        }
    )
    
    # Round 2 - Park (150 points)
    tracker.add_round(
        selected_project=2,
        effective_votes={2: 1.0},  # Only Voter 2 supports Park
        voter_budgets={
            1: 50,   # Voter 1: Unchanged
            2: 0     # Voter 2: 150 - 150 = 0
        }
    )
    
    # Create visualization data with proper voter preferences
    winners = {1: 100, 2: 150}  # Projects and their costs
    output = CustomBudgetAllocation(
        selected_projects=winners,
        round_tracker=tracker,
        projects_meta=projects,
        voter_preferences=voter_preferences
    )
    
    # Print visualization-ready data
    print("\nStarting State:")
    print("Total Budget: 300")
    print("Voter 1: 150 points (wants ONLY Library - 100 points)")
    print("Voter 2: 150 points (wants ONLY Park - 150 points)")
    
    for i, iteration in enumerate(output.details.iterations, 1):
        print(f"\nRound {i} (Pabutools Format):")
        project = iteration.selected_project
        print(f"Selected: {project.project.name} ({project.cost} points)")
        
        # Show supporters based on project name
        if project.name == "1":  # Library
            print("Supporters: [1]")  # Only Voter 1
        else:  # Park
            print("Supporters: [2]")  # Only Voter 2
            
        print(f"Voter budgets: {iteration.voters_budget}")
        
        # Show available projects
        if i == 1:
            print("Available projects: ['Park (150)']")
        else:
            print("Available projects: []")  # No projects left after Round 2

if __name__ == "__main__":
    run_adapter_example()
