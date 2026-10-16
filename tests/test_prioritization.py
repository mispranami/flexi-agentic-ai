"""
Unit Tests for Prioritization Tool

Tests the core prioritization logic:
- Different deadline scenarios
- Various available study hours
- Error handling for invalid inputs
- Edge cases (overdue, missing fields, etc.)
"""

import pytest
from datetime import datetime, timedelta
from src.prioritization_tool import PrioritizationTool, Assignment


class TestPrioritizationTool:
    """Test suite for the PrioritizationTool class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.tool = PrioritizationTool(available_hours_per_day=3.0)

    def test_parse_date_yyyy_mm_dd(self):
        """Test parsing of YYYY-MM-DD format."""
        date = self.tool.parse_date("2024-12-25")
        assert date.year == 2024
        assert date.month == 12
        assert date.day == 25

    def test_parse_date_dd_mm_yyyy(self):
        """Test parsing of DD/MM/YYYY format."""
        date = self.tool.parse_date("25/12/2024")
        assert date.year == 2024
        assert date.month == 12
        assert date.day == 25

    def test_parse_date_invalid_format(self):
        """Test that invalid date format raises ValueError."""
        with pytest.raises(ValueError):
            self.tool.parse_date("12-25-2024")  # Wrong format

    def test_prioritize_basic_scenarios(self):
        """
        TEST 1: Basic prioritization - verify assignments are sorted by urgency.
        
        Scenario:
        - Assignment A: Due in 1 day, 2 hours
        - Assignment B: Due in 5 days, 2 hours
        - Assignment C: Due in 10 days, 2 hours
        
        Expected: A > B > C (A is most urgent)
        """
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        next_week = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        two_weeks = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

        assignments = [
            {"name": "Assignment C", "deadline": two_weeks, "hours": 2, "category": "general"},
            {"name": "Assignment A", "deadline": tomorrow, "hours": 2, "category": "general"},
            {"name": "Assignment B", "deadline": next_week, "hours": 2, "category": "general"},
        ]

        result = self.tool.prioritize_assignments(assignments)

        # Verify order
        assert result[0]["assignment_name"] == "Assignment A"
        assert result[1]["assignment_name"] == "Assignment B"
        assert result[2]["assignment_name"] == "Assignment C"
        
        # Verify urgency scores are descending
        assert result[0]["urgency_score"] > result[1]["urgency_score"]
        assert result[1]["urgency_score"] > result[2]["urgency_score"]
        
        print("✓ TEST 1 PASSED: Basic prioritization by deadline")

    def test_prioritize_with_hours_variation(self):
        """
        TEST 2: Prioritization considers effort - same deadline but different hours.
        
        Scenario:
        - Assignment A: Due in 3 days, 10 hours
        - Assignment B: Due in 3 days, 2 hours
        
        Expected: A should be more urgent (higher effort)
        """
        deadline = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")

        assignments = [
            {"name": "Light Assignment", "deadline": deadline, "hours": 2, "category": "general"},
            {"name": "Heavy Assignment", "deadline": deadline, "hours": 10, "category": "general"},
        ]

        result = self.tool.prioritize_assignments(assignments)

        # Heavy assignment should come first
        assert result[0]["assignment_name"] == "Heavy Assignment"
        assert result[1]["assignment_name"] == "Light Assignment"
        
        print("✓ TEST 2 PASSED: Prioritization considers effort intensity")

    def test_prioritize_with_complexity_factor(self):
        """
        TEST 3: Prioritization considers assignment category/complexity.
        
        Scenario:
        - Exam: Due in 7 days, 5 hours (complexity factor 1.5)
        - Project: Due in 7 days, 5 hours (complexity factor 1.3)
        - General: Due in 7 days, 5 hours (complexity factor 1.0)
        
        Expected: Exam > Project > General (same deadline and hours, but different complexity)
        """
        deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        assignments = [
            {"name": "General Task", "deadline": deadline, "hours": 5, "category": "general"},
            {"name": "Exam Prep", "deadline": deadline, "hours": 5, "category": "exam"},
            {"name": "Project", "deadline": deadline, "hours": 5, "category": "project"},
        ]

        result = self.tool.prioritize_assignments(assignments)

        # Verify complexity-based ordering
        assert result[0]["assignment_name"] == "Exam Prep"
        assert result[1]["assignment_name"] == "Project"
        assert result[2]["assignment_name"] == "General Task"
        
        print("✓ TEST 3 PASSED: Prioritization considers complexity factor")

    def test_error_handling_missing_fields(self):
        """Test that missing required fields raise appropriate errors."""
        assignments = [
            {"name": "Assignment", "deadline": "2024-12-25"}  # Missing 'hours'
        ]

        with pytest.raises(ValueError) as exc_info:
            self.tool.prioritize_assignments(assignments)
        
        assert "missing required fields" in str(exc_info.value)
        print("✓ Error handling for missing fields works")

    def test_error_handling_invalid_hours(self):
        """Test that invalid hours raise appropriate errors."""
        deadline = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        # Negative hours
        assignments = [
            {"name": "Assignment", "deadline": deadline, "hours": -5, "category": "general"}
        ]

        with pytest.raises(ValueError) as exc_info:
            self.tool.prioritize_assignments(assignments)
        
        assert "cannot be negative" in str(exc_info.value).lower()
        
        # Unrealistically high hours
        assignments = [
            {"name": "Assignment", "deadline": deadline, "hours": 200, "category": "general"}
        ]

        with pytest.raises(ValueError) as exc_info:
            self.tool.prioritize_assignments(assignments)
        
        assert "too high" in str(exc_info.value).lower()
        
        print("✓ Error handling for invalid hours works")

    def test_empty_assignments_list(self):
        """Test handling of empty assignments list."""
        result = self.tool.prioritize_assignments([])
        assert result == []
        print("✓ Empty assignments list handled correctly")

    def test_overdue_assignment(self):
        """Test that overdue assignments get highest priority."""
        yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
        future = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")

        assignments = [
            {"name": "Future Task", "deadline": future, "hours": 5, "category": "general"},
            {"name": "Overdue", "deadline": yesterday, "hours": 1, "category": "general"},
        ]

        result = self.tool.prioritize_assignments(assignments)

        # Overdue should come first (has urgency_score of 1000)
        assert result[0]["assignment_name"] == "Overdue"
        assert result[0]["days_remaining"] < 0  # Negative means overdue
        assert result[0]["urgency_score"] == 1000  # Hardcoded high score for overdue
        
        print("✓ Overdue assignments get highest priority")

    def test_urgency_score_calculation(self):
        """Test that urgency score is calculated correctly."""
        # Use a specific date further in future to avoid day-of-boundary issues
        deadline = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        assignment_obj = Assignment(
            name="Test Assignment",
            deadline_date=deadline,
            estimated_hours=9.0,
            category="general"
        )

        score_data = self.tool.calculate_urgency_score(assignment_obj)

        # Verify structure
        assert "urgency_score" in score_data
        assert "effort_intensity" in score_data
        assert "days_remaining" in score_data
        assert "complexity_factor" in score_data

        # Verify values are reasonable
        assert score_data["urgency_score"] > 0
        assert score_data["effort_intensity"] > 0
        assert score_data["days_remaining"] >= 4  # At least 4 days (may be 5 if same time)
        
        print("✓ Urgency score calculated correctly")


# Run all tests with detailed output
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
