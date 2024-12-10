"""
Adapter module for integrating pabutools library with Method of Equal Shares (MES) implementation.
Provides utilities for data conversion, validation, and visualization functionality.
"""

from typing import Dict, List, Tuple, Optional
import logging
from pathlib import Path
import traceback
from dataclasses import dataclass
from gmpy2 import mpq

# Import core pabutools classes:
# - Project: Represents a votable item with cost and name
# - Instance: Collection of projects and budget constraints 
# - ApprovalBallot: A voter's set of approved projects
# - ApprovalProfile: Collection of all voters' ballots
# - Cost_Sat: Measures voter satisfaction based on project costs
from pabutools.election import Project, Instance, ApprovalBallot, ApprovalProfile, Cost_Sat
from pabutools.rules import method_of_equal_shares, BudgetAllocation
from pabutools.visualisation.visualisation import MESVisualiser

# Constants for validation
REQUIRED_META_FIELDS = ['num_votes', 'budget', 'num_voters', 'votes_per_project']
REQUIRED_PROJECT_FIELDS = ['name', 'cost', 'description', 'category']

logger = logging.getLogger("equal_shares_logger")

@dataclass
class MESResult:
    """Data class for MES algorithm results"""
    status: str
    results: Dict[int, float]
    visualization_path: str
    selected_projects: List[int]
    total_cost: float
    budget_per_voter: float
    error: Optional[str] = None
    traceback: Optional[str] = None

class ValidationError(Exception):
    """Custom exception for data validation errors."""
    pass

def validate_input_data(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: float,
    bids: dict[int, dict[int, int]]
) -> None:
    """
    Validate input data before conversion to pabutools format.
    
    Args:
        voters: List of voter IDs
        projects_costs: Dictionary mapping project IDs to costs
        budget: Total budget
        bids: Nested dictionary mapping project IDs to voter IDs and bid amounts
        
    Raises:
        ValidationError: If validation fails
    
    Example:
        >>> validate_input_data([1, 2], {101: 100}, 150.0, {101: {1: 1}})  # Valid
        >>> validate_input_data([], {}, 0, {})  # Raises ValidationError
        ValidationError: "Voters list cannot be empty"
    """
    if not voters:
        raise ValidationError("Voters list cannot be empty")
    if not projects_costs:
        raise ValidationError("Projects costs dictionary cannot be empty")
    if budget <= 0:
        raise ValidationError("Budget must be positive")
    if not bids:
        raise ValidationError("Bids dictionary cannot be empty")
    
    # Validate project IDs consistency
    project_ids = set(projects_costs.keys())
    bid_project_ids = set(bids.keys())
    if project_ids != bid_project_ids:
        raise ValidationError("Project IDs in costs and bids must match")
    
    # Validate voter IDs consistency
    voter_ids = set(voters)
    bid_voter_ids = set(voter_id for project_bids in bids.values() 
                       for voter_id in project_bids.keys())
    if not bid_voter_ids.issubset(voter_ids):
        raise ValidationError("All bidding voters must be in voters list")
        
    # Validate costs are positive
    if any(cost <= 0 for cost in projects_costs.values()):
        raise ValidationError("All project costs must be positive")
        
    # Validate budget is sufficient for at least one project
    if budget < min(projects_costs.values()):
        raise ValidationError("Budget must be sufficient for at least one project")

def validate_pabutools_data(
    instance: Instance,
    profile: ApprovalProfile
) -> None:
    """
    Validate pabutools data structures and metadata.
    
    Args:
        instance: Pabutools Instance object
        profile: Pabutools ApprovalProfile object
        
    Raises:
        ValidationError: If validation fails
    """
    if not hasattr(instance, 'project_meta'):
        raise ValidationError("Missing project_meta in instance")
    if not isinstance(instance.project_meta, dict):
        raise ValidationError("project_meta must be a dictionary")
        
    for project_id, meta in instance.project_meta.items():
        missing_fields = [field for field in REQUIRED_PROJECT_FIELDS if field not in meta]
        if missing_fields:
            raise ValidationError(
                f"Missing required fields {missing_fields} in metadata for project {project_id}"
            )
    
    missing_meta = [field for field in REQUIRED_META_FIELDS if field not in instance.meta]
    if missing_meta:
        raise ValidationError(f"Missing required fields {missing_meta} in instance metadata")
        
    if not hasattr(instance, 'budget_limit') or not instance.budget_limit:
        raise ValidationError("Instance must have a non-zero budget_limit")

def process_mes_results(
    instance: Instance,
    outcome: BudgetAllocation
) -> Tuple[Dict[int, float], float]:
    """
    Process MES algorithm results and calculate project allocations.
    
    Args:
        instance: Pabutools Instance containing all projects
        outcome: BudgetAllocation containing selected projects
        
    Returns:
        Tuple containing:
            - Dict mapping project IDs to their allocations (cost if selected, 0 if not)
            - Total cost of all selected projects
    """
    results = {}
    total_cost = 0
    
    for project in instance:
        project_id = int(project.name)
        if project in outcome:
            project_cost = float(project.cost)
            results[project_id] = project_cost
            total_cost += project_cost
        else:
            results[project_id] = 0
            
    return results, total_cost

def convert_to_pabutools_format(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: float,
    bids: dict[int, dict[int, int]]
) -> Tuple[Instance, ApprovalProfile]:
    """
    Convert system data format to pabutools format with metadata.
    
    Args:
        voters: List of voter IDs
        projects_costs: Dictionary mapping project IDs to costs
        budget: Total budget
        bids: Nested dictionary mapping project IDs to voter IDs and bid amounts
        
    Returns:
        Tuple containing:
            - Instance: Pabutools Instance with all projects and metadata
            - ApprovalProfile: Pabutools ApprovalProfile with all voter ballots

    Example:
        >>> voters = [1, 2]
        >>> costs = {101: 100, 102: 150}
        >>> budget = 200.0
        >>> bids = {101: {1: 1}, 102: {2: 1}}
        >>> instance, profile = convert_to_pabutools_format(
        ...     voters, costs, budget, bids
        ... )
        >>> len(instance)  # Number of projects
        2
    """
    try:
        validate_input_data(voters, projects_costs, budget, bids)
        
        projects = {}
        project_meta = {}
        instance = Instance()
        
        # Convert budget to mpq for precise rational arithmetic
        budget_mpq = mpq(str(budget))
        instance.budget_limit = budget_mpq
                
        # Convert projects and build metadata
        for project_id, cost in projects_costs.items():
            project_cost = mpq(str(cost))
            project = Project(str(project_id), project_cost)
            projects[project_id] = project
            instance.add(project)
            
            project_meta[str(project_id)] = {
                'name': str(project_id),
                'cost': float(project_cost),
                'description': f'Project {project_id}',
                'category': 'default'
            }
        
        instance.project_meta = project_meta
        
        # Create approval ballots (1 = approve)
        profile = ApprovalProfile()
        for voter_id in voters:
            ballot_projects = []
            # Add projects that this voter approved (bid > 0)
            for project_id, project_bids in bids.items():
                if voter_id in project_bids and project_bids[voter_id] > 0:
                    ballot_projects.append(projects[project_id])
            profile.append(ApprovalBallot(ballot_projects))
        
        # Calculate voting statistics
        votes_per_project = {
            str(project_id): sum(1 for voter_id in voters if voter_id in project_bids)
            for project_id, project_bids in bids.items()
        }
        
        total_votes = sum(votes_per_project.values())
        budget_per_voter = float(budget_mpq) / len(voters)
        
        # Set instance metadata
        instance.meta = {
            "budget": float(budget_mpq),
            "num_voters": len(voters),
            "num_votes": total_votes,
            "votes_per_project": votes_per_project,
            "total_cost": float(sum(mpq(str(cost)) for cost in projects_costs.values())),
            "avg_project_cost": float(sum(mpq(str(cost)) for cost in projects_costs.values())) / len(projects_costs),
            "max_project_cost": float(max(projects_costs.values())),
            "min_project_cost": float(min(projects_costs.values())),
            "description": "Student Union Budget",
            "currency": "ILS",
            "budget_per_voter": budget_per_voter
        }
        
        validate_pabutools_data(instance, profile)
        
        logger.info("Successfully converted data to pabutools format")
        logger.info(f"Number of voters in profile: {len(profile)}")
        logger.info(f"Number of projects: {len(instance)}")
        logger.info(f"Total votes: {total_votes}")
        logger.info(f"Budget per voter: {budget_per_voter}")
        logger.info(f"Votes per project: {votes_per_project}")
        
        return instance, profile
        
    except Exception as e:
        logger.error(f"Error in data conversion: {str(e)}")
        raise

def run_mes_visualization(
    voters: list[int],
    projects_costs: dict[int, int],
    budget: float, 
    bids: dict[int, dict[int, int]],
    output_path: str
) -> MESResult:
    """
    Run MES algorithm and generate visualization.
    
    Args:
        voters: List of voter IDs
        projects_costs: Dictionary mapping project IDs to costs
        budget: Total budget
        bids: Nested dictionary mapping project IDs to voter IDs and bid amounts
        output_path: Path where visualization files will be saved

    Returns:
        MESResult containing allocation results and visualization details
    """
    try:
        # Create output directory if it doesn't exist
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        # Convert data and run MES algorithm
        instance, profile = convert_to_pabutools_format(
            voters, projects_costs, budget, bids
        )
        
        logger.info("Running MES algorithm...")
        outcome = method_of_equal_shares(
            instance=instance,
            profile=profile,
            sat_class=Cost_Sat,
            analytics=True,
            verbose=True
        )
        
        logger.info("Generating visualization...")
        visualizer = MESVisualiser(
            profile=profile,
            instance=instance,
            outcome=outcome,
            verbose=True
        )
        
        # Generate HTML files showing the round-by-round MES execution and results summary
        visualizer.render(output_path)
        
        # Process results
        results, total_cost = process_mes_results(instance, outcome)
        logger.info(f"Total cost of selected projects: {total_cost}")
        
        return MESResult(
            status="success",
            results=results,
            visualization_path=output_path,
            selected_projects=[int(p.name) for p in outcome],
            total_cost=total_cost,
            budget_per_voter=instance.meta["budget_per_voter"]
        )
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Error in MES visualization: {error_msg}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        return MESResult(
            status="error",
            results={},
            visualization_path="",
            selected_projects=[],
            total_cost=0,
            budget_per_voter=0,
            error=error_msg,
            traceback=traceback.format_exc()
        )

#------------------------------------------------------------------------------
# Example Usage
#------------------------------------------------------------------------------

def example_usage():
    """Example showing how to use the adapter with sample data"""
    
    # Sample election data
    voters = [1, 2, 3]
    projects_costs = {
        101: 100,  # Project costs in currency units
        102: 150,
        103: 200
    }
    budget = 300.0  # Total budget
    # Approval votes (1 = approve, not in dict = disapprove)
    bids = {
        101: {1: 1, 2: 1},  # Voters 1 and 2 approve
        102: {2: 1, 3: 1},  # Voters 2 and 3 approve
        103: {1: 1, 3: 1}   # Voters 1 and 3 approve
    }
    
    try:
        # Test data conversion
        instance, profile = convert_to_pabutools_format(
            voters, projects_costs, budget, bids
        )
        print("\nData conversion test:")
        print(f"Number of projects: {len(instance)}")
        print(f"Number of voters: {len(profile)}")
        print(f"Budget per voter: {instance.meta['budget_per_voter']}")
        print(f"Total votes: {instance.meta['num_votes']}")
        print(f"Votes per project: {instance.meta['votes_per_project']}")
        
        # Run MES and generate visualization
        result = run_mes_visualization(
            voters=voters,
            projects_costs=projects_costs,
            budget=budget,
            bids=bids,
            output_path="./visualization_output"
        )
        
        print("\nVisualization test:")
        if result.status == "success":
            print("Visualization generated successfully!")
            print("\nProject allocations:")
            for project_id, amount in result.results.items():
                print(f"Project {project_id}: {amount}")
            print(f"\nSelected projects: {result.selected_projects}")
            print(f"Total cost: {result.total_cost}")
            print(f"Budget per voter: {result.budget_per_voter}")
            print(f"\nVisualization files saved to: {result.visualization_path}")
        else:
            print(f"Error: {result.error}")
            if result.traceback:
                print(f"Traceback: {result.traceback}")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    example_usage()
