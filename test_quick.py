#!/usr/bin/env python3
"""Quick test of the AI Study Planner - runs without Streamlit"""

import sys
sys.path.insert(0, '/Users/pranamimishra/Desktop/flexi')

from src.prioritization_tool import PrioritizationTool
from src.agent import StudyPlannerAgent
from datetime import datetime, timedelta

print("="*70)
print("AI STUDY PLANNER - QUICK TEST")
print("="*70)

# Test 1: Prioritization tool
print("\n[TEST 1] Prioritization Tool")
print("-" * 70)

tool = PrioritizationTool()
assignments = [
    {
        "name": "Physics Exam",
        "deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "hours": 8,
        "category": "exam"
    },
    {
        "name": "AI Project",
        "deadline": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "hours": 6,
        "category": "project"
    },
    {
        "name": "Math HW",
        "deadline": (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d"),
        "hours": 2,
        "category": "general"
    }
]

try:
    prioritized = tool.prioritize_assignments(assignments)
    print("✅ Prioritization tool works!")
    print("\nPrioritized assignments:")
    for i, item in enumerate(prioritized, 1):
        print(f"   {i}. {item['assignment_name']} (urgency: {item['urgency_score']})")
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test 2: Agent initialization
print("\n[TEST 2] Agent Initialization")
print("-" * 70)

try:
    agent = StudyPlannerAgent()
    print("✅ Agent initialized successfully")
    print(f"   Model: Gemini")
except Exception as e:
    print(f"❌ Error initializing agent: {e}")
    print("   Make sure .env has your GOOGLE_API_KEY")
    sys.exit(1)

# Test 3: Generate study plan
print("\n[TEST 3] Generating Study Plan")
print("-" * 70)

try:
    print("⏳ Calling Gemini API (this may take 5-10 seconds)...")
    result = agent.plan_study_schedule(assignments, available_hours=4.0)
    
    if result["success"]:
        print("✅ Study plan generated successfully!")
        print(f"\n📋 Prioritized {len(result['prioritized_assignments'])} assignments")
        print(f"\n📅 Study Plan (first 500 characters):")
        print("-" * 70)
        print(result['ai_generated_plan'][:500])
        print("...")
        print("-" * 70)
        print("\n✅ ALL TESTS PASSED!")
        print("\nYour application is working correctly.")
        print("Now run: streamlit run app.py")
    else:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print("\n" + "="*70)
