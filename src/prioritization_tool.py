"""
Prioritization Tool for Study Planner Agent

This module implements a rule-based prioritization algorithm that sorts assignments
based on urgency. It is NOT an AI component - it's a deterministic tool that the
AI agent will use to inform its planning decisions.

The prioritization logic considers:
1. Days until deadline (most important)
2. Assignment complexity (estimated from name or category)
3. Available study hours vs estimated hours needed
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Assignment:
    """Represents a single assignment with metadata."""
    name: str
    deadline_date: str  # Format: "YYYY-MM-DD" or "DD/MM/YYYY"
    estimated_hours: float
    category: str = "general"  # general, project, exam, report


class PrioritizationTool:
    """
    A deterministic tool that prioritizes assignments based on deadlines and effort.
    Used by the AI agent to create personalized study plans.
    """

    def __init__(self, available_hours_per_day: float = 3.0):
        """
        Initialize the prioritization tool.
        
        Args:
            available_hours_per_day: Total hours available for studying per day
        """
        self.available_hours_per_day = available_hours_per_day

    def parse_date(self, date_str: str) -> datetime:
        """
        Parse date string in multiple formats.
        
        Args:
            date_str: Date string in "YYYY-MM-DD" or "DD/MM/YYYY" format
            
        Returns:
            datetime object
            
        Raises:
            ValueError: If date format is invalid
        """
        # Try YYYY-MM-DD format first
        try:
            return datetime.strptime(date_str.strip(), "%Y-%m-%d")
        except ValueError:
            pass
        
        # Try DD/MM/YYYY format
        try:
            return datetime.strptime(date_str.strip(), "%d/%m/%Y")
        except ValueError:
            raise ValueError(
                f"Invalid date format: {date_str}. "
                "Please use YYYY-MM-DD or DD/MM/YYYY format."
            )

    def calculate_urgency_score(self, assignment: Assignment) -> Dict[str, Any]:
        """
        Calculate an urgency score for a single assignment.
        
        Score components:
        - days_remaining: How many days until deadline (lower = more urgent)
        - complexity_factor: Multiplier based on assignment type (1.0 to 1.5)
        - effort_intensity: Hours needed per day if we want to finish on time
        
        Args:
            assignment: Assignment object
            
        Returns:
            Dictionary with breakdown of urgency calculation
        """
        today = datetime.now()
        deadline = self.parse_date(assignment.deadline_date)
        
        days_remaining = (deadline - today).days
        
        if days_remaining < 0:
            days_remaining = -1  # Overdue
        
        # Complexity factor - some assignments naturally take more effort
        complexity_factors = {
            "exam": 1.5,      # Exams are complex
            "project": 1.3,   # Projects take more effort
            "report": 1.2,    # Reports moderate effort
            "general": 1.0    # General tasks baseline
        }
        complexity_factor = complexity_factors.get(assignment.category, 1.0)
        
        # Effort intensity: how many hours/day needed to complete on time
        effort_intensity = assignment.estimated_hours / max(days_remaining, 1)
        
        # Calculate urgency score
        # Lower days_remaining = higher score
        # Higher effort_intensity = higher score
        if days_remaining <= 0:
            urgency_score = 1000  # Overdue tasks get highest urgency
        else:
            urgency_score = (effort_intensity * complexity_factor * 100) / (days_remaining + 1)
        
        return {
            "assignment_name": assignment.name,
            "days_remaining": days_remaining,
            "estimated_hours": assignment.estimated_hours,
            "complexity_factor": complexity_factor,
            "effort_intensity": round(effort_intensity, 2),
            "urgency_score": round(urgency_score, 2),
            "category": assignment.category,
        }

    def prioritize_assignments(
        self, assignments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Main tool function: Prioritize assignments by urgency.
        
        This is the primary function the AI agent will call.
        
        Args:
            assignments: List of dicts with keys:
                        - name: Assignment name
                        - deadline: Date in "YYYY-MM-DD" or "DD/MM/YYYY"
                        - hours: Estimated hours needed
                        - category: (optional) "exam", "project", "report", or "general"
        
        Returns:
            List of assignments sorted by urgency (highest first) with urgency breakdown
            
        Raises:
            ValueError: If any assignment has missing required fields
        """
        if not assignments:
            return []
        
        # Validate and convert input
        assignment_objects = []
        for idx, item in enumerate(assignments):
            try:
                # Validate required fields
                if "name" not in item or "deadline" not in item or "hours" not in item:
                    raise ValueError(
                        f"Assignment {idx} missing required fields. "
                        "Need: name, deadline, hours"
                    )
                
                assignment = Assignment(
                    name=str(item["name"]).strip(),
                    deadline_date=str(item["deadline"]).strip(),
                    estimated_hours=float(item["hours"]),
                    category=str(item.get("category", "general")).lower()
                )
                
                # Validate values
                if assignment.estimated_hours < 0:
                    raise ValueError(f"Hours cannot be negative for {assignment.name}")
                
                if assignment.estimated_hours > 100:
                    raise ValueError(f"Hours seems too high for {assignment.name}")
                
                assignment_objects.append(assignment)
            
            except (KeyError, ValueError, TypeError) as e:
                raise ValueError(f"Error processing assignment {idx}: {str(e)}")
        
        # Calculate urgency scores for all assignments
        scored_assignments = []
        for assignment in assignment_objects:
            score_breakdown = self.calculate_urgency_score(assignment)
            scored_assignments.append(score_breakdown)
        
        # Sort by urgency score (descending - highest urgency first)
        prioritized = sorted(
            scored_assignments,
            key=lambda x: x["urgency_score"],
            reverse=True
        )
        
        return prioritized


def create_tool_result_summary(prioritized_list: List[Dict[str, Any]]) -> str:
    """
    Create a human-readable summary of prioritization results.
    
    Args:
        prioritized_list: Output from prioritize_assignments()
        
    Returns:
        Formatted string summary
    """
    if not prioritized_list:
        return "No assignments to prioritize."
    
    summary = "📋 PRIORITIZED ASSIGNMENTS:\n"
    summary += "=" * 60 + "\n\n"
    
    for idx, item in enumerate(prioritized_list, 1):
        summary += f"{idx}. {item['assignment_name']}\n"
        summary += f"   Category: {item['category'].capitalize()}\n"
        summary += f"   Days remaining: {item['days_remaining']}\n"
        summary += f"   Estimated hours: {item['estimated_hours']}\n"
        summary += f"   Daily effort needed: {item['effort_intensity']} hrs/day\n"
        summary += f"   Urgency score: {item['urgency_score']}\n"
        summary += "\n"
    
    return summary
