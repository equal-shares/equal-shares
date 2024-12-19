"""Example using algorithm wrapper for visualization"""
from dataclasses import dataclass
from src.algorithm.mes_visualization.algorithm_wrapper import (
    run_algorithm_with_tracking,
    create_visualization_output
)

@dataclass
class Project:
    """Simple project class for example"""
    project_id: int
    name: str
    min_points: int
    description: str

def run_wrapper_example():
    """
    Scenario:
    - Total budget: 300
    - Initial per voter: 300/2 = 150 each
    - Voter 1 wants ONLY Library (100 points)
    - Voter 2 wants ONLY Park (150 points)
    """
    # Two voters
    voters = [1, 2]
    
    # Two projects with costs
    projects_costs = {
        1: 100,  # Library
        2: 150   # Park
    }
    
    # Voter preferences - each wants only one project
    bids = {
        1: {  # Project 1 (Library)
            1: 100,  # Voter 1 bids full cost
            2: 0     # Voter 2 doesn't want Library
        },
        2: {  # Project 2 (Park)
            1: 0,    # Voter 1 doesn't want Park
            2: 150   # Voter 2 bids full cost
        }
    }
    
    # Create project metadata for visualization
    projects_meta = {
        1: Project(1, "Library", 100, "Public library upgrade"),
        2: Project(2, "Park", 150, "Community park development")
    }
    
    # Run algorithm with tracking
    winners, tracker = run_algorithm_with_tracking(
        voters=voters,
        projects_costs=projects_costs,
        budget=300,
        bids=bids
    )
    
    # Create visualization output
    output = create_visualization_output(
        winners=winners,
        tracker=tracker,
        projects_meta=projects_meta
    )

    print(f'winners: {winners}')
    print(f'tracker: {tracker}')
    print(f'output: {output}')

    # # Print visualization-ready data
    # print("\nStarting State:")
    # print("Total Budget: 300")
    # print("Voter 1: 150 points (wants ONLY Library - 100 points)")
    # print("Voter 2: 150 points (wants ONLY Park - 150 points)")
    
    # print("\nAlgorithm Results:")
    # print(f"Selected projects: {winners}")
    # print(f"Number of rounds: {len(tracker.rounds)}")
    
    # for i, round_info in enumerate(tracker.rounds, 1):
    #     print(f"\nRound {i}:")
    #     project = projects_meta[round_info.selected_project]
    #     print(f"Selected: {project.name} ({project.min_points} points)")
    #     print(f"Effective votes: {round_info.effective_votes}")
    #     print(f"Voter budgets: {round_info.voter_budgets}")
    #     print(f"Remaining budget: {round_info.remaining_budget}")

    #     # Show remaining projects
    #     remaining = []
    #     if i == 1:
    #         remaining.append(f"Park ({projects_costs[2]})")
    #     print(f"Available projects: {remaining}")

if __name__ == "__main__":
    run_wrapper_example()
