"""
Adapter module for integrating pabutools library with Method of Equal Shares (MES) implementation.
Provides utilities for data conversion, validation, and visualization functionality.
"""

from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import traceback
from gmpy2 import mpq

from pabutools.election import (
    Project,
    Instance,
    ApprovalBallot,
    ApprovalProfile,
    Cost_Sat
)
from pabutools.rules import method_of_equal_shares, BudgetAllocation
from pabutools.visualisation.visualisation import MESVisualiser

from src.logger import get_logger, LoggerName

logger = get_logger(LoggerName.ALGORITHM)
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)

# Validation schemas
REQUIRED_META_FIELDS = ['num_votes', 'budget', 'num_voters', 'votes_per_project']
REQUIRED_PROJECT_FIELDS = ['name', 'cost', 'description', 'category']

@dataclass
class MESResult:
    """Data class for MES algorithm results."""
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

def extract_voters_from_votes(votes: List[Any]) -> List[int]:
    """Extract unique voter IDs from votes data."""
    return list({vote.voter.voter_id for vote in votes})

def create_bids_from_votes(votes: List[Any]) -> Dict[int, Dict[int, int]]:
    """Convert vote data to bids format (1 for approval, 0 for disapproval)."""
    bids: Dict[int, Dict[int, int]] = {}
    
    for vote in votes:
        voter_id = vote.voter.voter_id
        for project_vote in vote.projects:
            project_id = project_vote.project_id
            if project_id not in bids:
                bids[project_id] = {}
            bids[project_id][voter_id] = 1 if project_vote.points > 0 else 0
    
    return bids

def validate_input_data(
    voters: List[int],
    projects: Dict[int, Any],
    budget: float,
    bids: Dict[int, Dict[int, int]]
) -> None:
    """
    Validate input data before conversion to pabutools format.
    
    Args:
        voters: List of voter IDs
        projects: Dictionary of Project objects with details
        budget: Total budget
        bids: Nested dictionary mapping project IDs to voter IDs and bid amounts
        
    Raises:
        ValidationError: If validation fails
    """
    if not voters:
        raise ValidationError("Voters list cannot be empty")
    if not projects:
        raise ValidationError("Projects dictionary cannot be empty")
    if budget <= 0:
        raise ValidationError("Budget must be positive")
    if not bids:
        raise ValidationError("Bids dictionary cannot be empty")
    
    # Validate project IDs consistency
    project_ids = set(projects.keys())
    bid_project_ids = set(bids.keys())
    if project_ids != bid_project_ids:
        raise ValidationError("Project IDs in projects and bids must match")
    
    # Validate voter IDs consistency
    voter_ids = set(voters)
    bid_voter_ids = {
        voter_id 
        for project_bids in bids.values() 
        for voter_id in project_bids
    }
    if not bid_voter_ids.issubset(voter_ids):
        raise ValidationError("All bidding voters must be in voters list")
        
    # Validate costs and budget
    project_costs = [p.min_points for p in projects.values()]
    if any(cost <= 0 for cost in project_costs):
        raise ValidationError("All project costs must be positive")
    if budget < min(project_costs):
        raise ValidationError("Budget must be sufficient for at least one project")

def calculate_voting_statistics(
    projects: Dict[int, Any],
    votes: List[Any]
) -> Tuple[Dict[str, int], int]:
    """
    Calculate voting statistics for projects.
    
    Args:
        projects: Dictionary mapping project IDs to project objects
        votes: List of vote objects
        
    Returns:
        Tuple containing:
            - Dictionary mapping project IDs to vote counts
            - Total number of votes
    """
    votes_per_project = {}
    for project_id in projects:
        votes_count = sum(
            1 for vote in votes
            for pv in vote.projects
            if pv.project_id == project_id and pv.points > 0
        )
        votes_per_project[str(project_id)] = votes_count
    
    return votes_per_project, sum(votes_per_project.values())

def create_instance_metadata(
    settings: Any,
    projects: Dict[int, Any],
    voters: List[int],
    votes_per_project: Dict[str, int],
    total_votes: int,
    budget: float
) -> Dict[str, Any]:
    """Create metadata for pabutools Instance."""
    project_costs = [mpq(str(p.min_points)) for p in projects.values()]
    return {
        "poll_id": settings.poll_id,
        "budget": float(budget),
        "num_voters": len(voters),
        "num_votes": total_votes,
        "votes_per_project": votes_per_project,
        "total_cost": float(sum(project_costs)),
        "avg_project_cost": float(sum(project_costs)) / len(projects),
        "max_project_cost": float(max(p.max_points for p in projects.values())),
        "min_project_cost": float(min(p.min_points for p in projects.values())),
        "description": "Participatory Budgeting Poll",
        "currency": "points",
        "budget_per_voter": float(budget) / len(voters) if voters else 0,
        "open_for_voting": settings.open_for_voting
    }

def convert_to_pabutools_format(
    settings: Any,
    projects: Dict[int, Any],
    votes: List[Any]
) -> Tuple[Instance, ApprovalProfile]:
    """
    Convert system data format to pabutools format with metadata.
    
    Args:
        settings: Poll settings object containing metadata
        projects: Dictionary of Project objects with details
        votes: List of VoteData objects containing voter info and project votes
        
    Returns:
        Tuple containing:
            - Instance: Pabutools Instance with all projects and metadata
            - ApprovalProfile: Pabutools ApprovalProfile with all voter ballots
    """
    try:
        print(f'settings: {settings}')
        print(f'projects: {projects}')
        print(f'votes: {votes}')

        # Extract and validate input data
        voters = extract_voters_from_votes(votes)
        budget = float(settings.max_total_points)
        bids = create_bids_from_votes(votes)
        
        validate_input_data(voters, projects, budget, bids)
        
        # Initialize pabutools objects
        instance = Instance()
        instance.budget_limit = mpq(str(budget))
        
        # Convert projects and build metadata
        projects_map = {}
        project_meta = {}
        
        for project_id, project_info in projects.items():
            project_cost = mpq(str(project_info.min_points))
            project = Project(str(project_id), project_cost)
            projects_map[project_id] = project
            instance.add(project)
            
            project_meta[str(project_id)] = {
                'name': project_info.name,
                'cost': float(project_cost),
                'description': project_info.description_1,
                'category': 'default',
                'min_points': project_info.min_points,
                'max_points': project_info.max_points,
                'created_at': project_info.created_at.isoformat()
            }
        
        instance.project_meta = project_meta
        
        # Create approval profile
        profile = ApprovalProfile()
        for vote_data in votes:
            approved_projects = [
                projects_map[pv.project_id]
                for pv in vote_data.projects
                if pv.points > 0
            ]
            profile.append(ApprovalBallot(approved_projects))
        
        # Calculate statistics and set metadata
        votes_per_project, total_votes = calculate_voting_statistics(projects, votes)
        instance.meta = create_instance_metadata(
            settings, projects, voters, 
            votes_per_project, total_votes, budget
        )
        
        logger.info(
            f"Data conversion complete - Poll: {settings.poll_id}, "
            f"Voters: {len(profile)}, Projects: {len(instance)}, "
            f"Total votes: {total_votes}"
        )
        
        print(f'instance: {instance}')
        print(f'profile: {profile}')

        return instance, profile
        
    except Exception as e:
        logger.error(f"Data conversion error: {str(e)}")
        raise

def process_mes_results(
    instance: Instance,
    outcome: BudgetAllocation
) -> Tuple[Dict[int, float], float]:
    """
    Process MES algorithm results and calculate allocations.
    
    Args:
        instance: Pabutools Instance containing all projects
        outcome: BudgetAllocation containing selected projects
        
    Returns:
        Tuple containing:
            - Dict mapping project IDs to their allocations (cost if selected, 0 if not)
            - Total cost of all selected projects
    """
    print(f'outcome: BudgetAllocation: {outcome}')
    results = {}
    total_cost = 0
    
    for project in instance:
        project_id = int(project.name)
        if project in outcome:
            cost = float(project.cost)
            results[project_id] = cost
            total_cost += cost
        else:
            results[project_id] = 0
            
    return results, total_cost

def run_mes_visualization(
    settings: Any,
    projects: Dict[int, Any],
    votes: List[Any],
    output_path: str
) -> MESResult:
    """
    Run MES algorithm and generate visualization.
    
    Args:
        settings: Poll settings object containing metadata
        projects: Dictionary of Project objects with details
        votes: List of VoteData objects containing voter info and project votes
        output_path: Path where visualization files will be saved

    Returns:
        MESResult containing allocation results and visualization details
    """
    try:
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        instance, profile = convert_to_pabutools_format(settings, projects, votes)
        
        logger.info("Running MES algorithm...")
        
        outcome = method_of_equal_shares(
            instance=instance,
            profile=profile,
            sat_class=Cost_Sat,
            analytics=True,
            verbose=False
        )

        logger.info(f'outcome type: {type(outcome)}')
        logger.info(f'outcome details: {dir(outcome)}')
        
        if not hasattr(outcome, 'details') or not hasattr(outcome.details, 'iterations'):
            logger.error("MES outcome doesn't have required details")
            logger.error(f"outcome attributes: {dir(outcome)}")
            if hasattr(outcome, 'details'):
                logger.error(f"details attributes: {dir(outcome.details)}")
            raise ValueError("Invalid MES outcome format")

        logger.info("Generating visualization...")
        visualizer = MESVisualiser(profile, instance, outcome, verbose=False)
        visualizer.render(output_path)
        
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
        return None