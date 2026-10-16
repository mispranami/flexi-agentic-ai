"""
Study Planner Agent using LangGraph and Google Gemini

This module implements an AI agent that:
1. Receives user assignments and available study hours
2. Uses the prioritization tool to sort assignments by urgency
3. Uses Google Gemini to generate a personalized, explanation-rich study plan

The agent workflow:
- Input validation and formatting
- Call prioritization tool (deterministic)
- Use Gemini to analyze results and create personalized plan
- Return structured response with reasoning
"""

import os
import json
from typing import Any, Dict, List
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

from src.prioritization_tool import PrioritizationTool, create_tool_result_summary

# Load environment variables
load_dotenv()


class StudyPlannerAgent:
    """
    AI Agent that creates personalized study plans using Groq LLM
    and the prioritization tool.
    """

    def __init__(self, api_key: str = None):
        """
        Initialize the agent.
        
        Args:
            api_key: Groq API key. If None, loads from GROQ_API_KEY env var.
        """
        if api_key is None:
            api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. Please set it in .env file or pass it directly."
            )
        
        # Initialize Groq client
        self.client = Groq(api_key=api_key)
        # Use available open-source models on Groq
        # These are the current available models
        self.model = "openai/gpt-oss-120b"
        self.prioritization_tool = PrioritizationTool()

    def plan_study_schedule(
        self,
        assignments: List[Dict[str, Any]],
        available_hours: float = 3.0,
    ) -> Dict[str, Any]:
        """
        Main agent function: Create a complete study plan.
        
        Workflow:
        1. Validate inputs
        2. Prioritize assignments using the tool
        3. Ask Gemini to create personalized study plan based on priorities
        4. Return structured response
        
        Args:
            assignments: List of assignment dicts with name, deadline, hours, category
            available_hours: Available study hours per day
            
        Returns:
            Dictionary with prioritized assignments and AI-generated study plan
        """
        try:
            # Validate inputs
            if not assignments:
                return {
                    "success": False,
                    "error": "No assignments provided",
                    "plan": None,
                    "prioritized_assignments": []
                }
            
            if available_hours <= 0 or available_hours > 24:
                return {
                    "success": False,
                    "error": f"Invalid available hours: {available_hours}. Must be between 0 and 24.",
                    "plan": None,
                    "prioritized_assignments": []
                }
            
            # Step 1: Use prioritization tool (deterministic)
            prioritized = self.prioritization_tool.prioritize_assignments(assignments)
            
            if not prioritized:
                return {
                    "success": False,
                    "error": "Could not prioritize assignments",
                    "plan": None,
                    "prioritized_assignments": []
                }
            
            # Step 2: Create context for Gemini
            tool_summary = create_tool_result_summary(prioritized)
            
            # Step 3: Ask Groq to generate personalized plan
            prompt = self._create_prompt(
                assignments=assignments,
                prioritized_list=prioritized,
                available_hours=available_hours,
                tool_summary=tool_summary
            )
            
            # Try to call Groq with fallback models if needed
            models_to_try = [
                "openai/gpt-oss-120b",      # Main model
                "openai/gpt-oss-20b",       # Faster fallback
                "qwen/qwen3.8-27b",         # Alternative
            ]
            
            study_plan = None
            last_error = None
            
            for model_name in models_to_try:
                try:
                    message = self.client.chat.completions.create(
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        model=model_name,
                        temperature=0.7,
                        max_tokens=2000,
                    )
                    study_plan = message.choices[0].message.content
                    break
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if study_plan is None:
                return {
                    "success": False,
                    "error": f"Could not generate plan. Error: {last_error}",
                    "plan": None,
                    "prioritized_assignments": prioritized
                }
            
            # Step 4: Return structured response
            return {
                "success": True,
                "error": None,
                "timestamp": datetime.now().isoformat(),
                "available_hours_per_day": available_hours,
                "total_assignments": len(assignments),
                "prioritized_assignments": prioritized,
                "tool_summary": tool_summary,
                "ai_generated_plan": study_plan,
                "plan": study_plan  # For backward compatibility
            }
        
        except ValueError as e:
            return {
                "success": False,
                "error": f"Validation error: {str(e)}",
                "plan": None,
                "prioritized_assignments": []
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error generating plan: {str(e)}",
                "plan": None,
                "prioritized_assignments": []
            }

    def _create_prompt(
        self,
        assignments: List[Dict[str, Any]],
        prioritized_list: List[Dict[str, Any]],
        available_hours: float,
        tool_summary: str
    ) -> str:
        """
        Create a detailed prompt for Gemini that includes:
        - Assignment details
        - Prioritization results (from tool)
        - Available study hours
        - Instructions for creating personalized plan
        
        Args:
            assignments: Original assignment list
            prioritized_list: Tool output (prioritized assignments)
            available_hours: Hours available per day
            tool_summary: Human-readable summary from tool
            
        Returns:
            Formatted prompt for Gemini
        """
        prompt = f"""
You are an expert study planning assistant. A student has provided you with their assignments and available study time.

AVAILABLE STUDY TIME PER DAY: {available_hours} hours

ASSIGNMENTS PROVIDED BY STUDENT:
{json.dumps(assignments, indent=2)}

PRIORITIZATION ANALYSIS (from automated tool):
{tool_summary}

YOUR TASK:
1. Review the prioritized list above - these are sorted by urgency (deadline pressure + complexity)
2. Create a DETAILED, PERSONALIZED study plan that:
   - Explains WHY each assignment is prioritized in this order (reference the urgency scores)
   - Allocates study time from the available {available_hours} hours/day
   - Provides specific study strategies for each assignment
   - Includes rest breaks and buffer time
   - Suggests which days to focus on which assignments
   - Gives actionable tips for time management
   - Addresses any potential conflicts or scheduling issues

3. Format your response clearly with:
   - A brief summary (2-3 sentences)
   - The prioritization reasoning
   - Day-by-day or weekly breakdown
   - Specific strategies for each assignment
   - Tips for staying on track

IMPORTANT: Be encouraging and realistic. The student is busy with internship work too.
"""
        return prompt

    def plan_study_schedule_with_feedback(
        self,
        assignments: List[Dict[str, Any]],
        available_hours: float = 3.0,
        user_feedback: str = None
    ) -> Dict[str, Any]:
        """
        Extended agent function that can incorporate user feedback.
        
        This allows for a conversational refinement of the study plan.
        
        Args:
            assignments: List of assignment dicts
            available_hours: Hours per day
            user_feedback: Optional feedback/constraints from user
            
        Returns:
            Dictionary with updated plan
        """
        # Get initial plan
        result = self.plan_study_schedule(assignments, available_hours)
        
        if not result["success"] or not user_feedback:
            return result
        
        # If user provided feedback, ask Gemini to refine the plan
        refinement_prompt = f"""
The student has provided feedback on the initial study plan:

STUDENT FEEDBACK:
{user_feedback}

PREVIOUS STUDY PLAN:
{result['ai_generated_plan']}

PRIORITIES (from automated tool - DON'T CHANGE):
{result['tool_summary']}

Please revise the study plan to address the student's feedback while keeping the assignment priorities the same.
Keep the same format and level of detail.
"""
        
        try:
            response = self.model.generate_content(refinement_prompt)
            result['ai_generated_plan'] = response.text
            result['plan'] = response.text
            result['user_feedback'] = user_feedback
            result['feedback_incorporated'] = True
        except Exception as e:
            result['feedback_error'] = str(e)
            result['feedback_incorporated'] = False
        
        return result
