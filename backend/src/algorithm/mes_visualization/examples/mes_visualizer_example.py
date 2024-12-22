"""
Example usage of the MES Visualizer module.
This file demonstrates how to use the visualizer with both custom and pabutools implementations.
"""

import datetime
import os
from pathlib import Path
from src.algorithm.mes_visualization.mes_visualizer import run_mes_visualization, MESImplementation

class ProjectVote:
    """Represents a single vote for a project."""
    def __init__(self, poll_id, voter_id, project_id, points, rank):
        self.poll_id = poll_id
        self.voter_id = voter_id
        self.project_id = project_id
        self.points = points
        self.rank = rank
        
    def __str__(self):
        return (f"ProjectVote(project_id={self.project_id}, "
                f"points={self.points}, rank={self.rank})")

class Voter:
    """Represents a voter."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def __str__(self):
        return (f"Voter(voter_id={self.voter_id}, "
                f"email='{self.email}', note='{self.note}')")

class VoteData:
    """Contains vote information."""
    def __init__(self, poll_id, voter, projects):
        self.poll_id = poll_id
        self.voter = voter
        self.projects = projects
        
    def __str__(self):
        projects_str = '\n    '.join(str(p) for p in self.projects)
        return (f"VoteData(\n  poll_id={self.poll_id},\n"
                f"  voter={self.voter},\n"
                f"  projects=[\n    {projects_str}\n  ])")

class Settings:
    """Holds poll configuration."""
    def __init__(self):
        self.poll_id = 1
        self.max_total_points = 1000
        self.points_step = 100
        self.open_for_voting = True
        self.results = None

class Project:
    """Represents a project that can be voted on."""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __str__(self):
        return f"Project(id={self.project_id}, name='{self.name}', min_points={self.min_points})"

def create_sample_data():
    """Create sample data structures for testing."""
    
    # Create sample settings
    settings = Settings()
    
    # Create sample projects
    projects = {
        1: Project(
            poll_id=1,
            project_id=1,
            name='Student Lounge Update',
            min_points=100,
            max_points=800,
            description_1='Renovate the main student lounge with new furniture and study areas',
            description_2='-',
            fixed=False,
            order_number=1,
            created_at=datetime.datetime(2024, 12, 11, 12, 41, 55, 596092)
        ),
        2: Project(
            poll_id=1,
            project_id=2,
            name='Research Lab Equipment',
            min_points=100,
            max_points=600,
            description_1='Purchase new microscopes and lab equipment for biology research',
            description_2='-',
            fixed=False,
            order_number=2,
            created_at=datetime.datetime(2024, 12, 11, 12, 41, 55, 616323)
        ),
        3: Project(
            poll_id=1,
            project_id=3,
            name='Campus Garden',
            min_points=100,
            max_points=1000,
            description_1='Create a sustainable garden on campus',
            description_2='-',
            fixed=False,
            order_number=3,
            created_at=datetime.datetime(2024, 12, 11, 12, 41, 55, 616370)
        )
    }
    
    # Create sample votes
    votes = [
        VoteData(
            poll_id=1,
            voter=Voter(
                poll_id=1,
                voter_id=1,
                email='voter1@example.com',
                note='voter1',
                created_at=datetime.datetime(2024, 12, 11, 12, 42, 36, 824080)
            ),
            projects=[
                ProjectVote(poll_id=1, voter_id=1, project_id=1, points=600, rank=1),
                ProjectVote(poll_id=1, voter_id=1, project_id=2, points=400, rank=2),
                ProjectVote(poll_id=1, voter_id=1, project_id=3, points=0, rank=3)
            ]
        ),
        VoteData(
            poll_id=1,
            voter=Voter(
                poll_id=1,
                voter_id=2,
                email='voter2@example.com',
                note='voter2',
                created_at=datetime.datetime(2024, 12, 11, 12, 43, 2, 113128)
            ),
            projects=[
                ProjectVote(poll_id=1, voter_id=2, project_id=1, points=700, rank=1),
                ProjectVote(poll_id=1, voter_id=2, project_id=2, points=300, rank=2),
                ProjectVote(poll_id=1, voter_id=2, project_id=3, points=0, rank=3)
            ]
        ),
        VoteData(
            poll_id=1,
            voter=Voter(
                poll_id=1,
                voter_id=3,
                email='voter3@example.com',
                note='voter3',
                created_at=datetime.datetime(2024, 12, 11, 12, 43, 2, 113128)
            ),
            projects=[
                ProjectVote(poll_id=1, voter_id=3, project_id=1, points=400, rank=2),
                ProjectVote(poll_id=1, voter_id=3, project_id=2, points=600, rank=1),
                ProjectVote(poll_id=1, voter_id=3, project_id=3, points=0, rank=3)
            ]
        )
    ]
    
    return settings, projects, votes

def run_implementation_test(
    settings, 
    projects, 
    votes, 
    implementation: MESImplementation,
    output_dir: Path
) -> None:
    """Run MES visualization with specified implementation."""
    print(f"\nTesting {implementation.value} implementation")
    print("-" * 40)
    
    # Create implementation-specific output directory
    output_path = output_dir / implementation.value
    
    # Run MES visualization
    result = run_mes_visualization(
        settings=settings,
        projects=projects,
        votes=votes,
        output_path=str(output_path),
        implementation=implementation
    )
    
    # Print results
    if result and result.status == "success":
        print("\nVisualization generated successfully!")
        print("\nProject allocations:")
        for project_id, amount in result.results.items():
            if amount > 0:
                project = projects[project_id]
                print(f"- {project.name}: {amount} points")
        
        print(f"\nTotal cost: {result.total_cost}")
        print(f"Budget per voter: {result.budget_per_voter}")
        print(f"Visualization saved to: {result.visualization_path}")
    else:
        print(f"\nError occurred: {result.error if result else 'Unknown error'}")
        if result and result.traceback:
            print(f"Traceback: {result.traceback}")

def run_example():
    """Run example usage of the MES visualizer with both implementations."""
    try:
        # Create sample data
        settings, projects, votes = create_sample_data()
        
        print("\nRunning MES Visualization Comparison")
        print("=" * 40)
        print(f"Number of projects: {len(projects)}")
        print(f"Number of voters: {len(votes)}")
        print(f"Total budget: {settings.max_total_points}")
        
        # Setup output directory
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Test custom implementation
        run_implementation_test(
            settings, 
            projects, 
            votes, 
            MESImplementation.CUSTOM,
            output_dir
        )
        
        # # Test pabutools implementation
        # run_implementation_test(
        #     settings, 
        #     projects, 
        #     votes, 
        #     MESImplementation.PABUTOOLS,
        #     output_dir
        # )
        
        print("\nComparison complete!")
        print(f"Results saved in: {output_dir}")
        
    except Exception as e:
        print(f"Error in example: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    run_example()
