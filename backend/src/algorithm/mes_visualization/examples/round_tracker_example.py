"""Example showing how voter budgets change during algorithm execution"""
from src.algorithm.mes_visualization.round_tracker import RoundTracker

def run_round_tracker_example():
    """
    Scenario:
    - Total budget: 300
    - Initial per voter: 300/2 = 150 each
    - Voter 1 wants ONLY Library (100 points)
    - Voter 2 wants ONLY Park (150 points)
    """
    # Initial state:
    # Voter 1: 150 points (wants Library only)
    # Voter 2: 150 points (wants Park only)
    tracker = RoundTracker(initial_budget=300)
    
    # Round 1 - Library (100 points)
    tracker.update_budget(cost=100)
    tracker.add_round(
        selected_project=1,
        effective_votes={1: 1.0},  # Only Voter 1 supports Library
        voter_budgets={
            1: 50,   # Voter 1: 150 - 100 (full Library cost) = 50
            2: 150   # Voter 2: Unchanged as they don't want Library
        }
    )
    
    # Round 2 - Park (200 points)
    tracker.update_budget(cost=200)
    tracker.add_round(
        selected_project=2,
        effective_votes={2: 1.0},  # Only Voter 2 supports Park
        voter_budgets={
            1: 50,   # Voter 1: Unchanged as they don't want Park
            2: 0     # Voter 2: 150 - 150 (Park cost) = 0
        }
    )
    
    # Print detailed state after each round
    print("\nStarting State:")
    print("Total Budget: 300")
    print("Voter 1: 150 points (wants ONLY Library - 100 points)")
    print("Voter 2: 150 points (wants ONLY Park - 150 points)")
    
    for i, round_info in enumerate(tracker.rounds, 1):
        print(f"\nRound {i}:")
        if round_info.selected_project == 1:
            print("Selected: Library (100 points)")
            print("Supported by: Voter 1 only")
        else:
            print("Selected: Park (150 points)")
            print("Supported by: Voter 2 only")
        print(f"Voter budgets: {round_info.voter_budgets}")
        print(f"Remaining total budget: {round_info.remaining_budget}")

if __name__ == "__main__":
    run_round_tracker_example()
