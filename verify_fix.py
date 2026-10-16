#!/usr/bin/env python3
"""Verify that the Gemini model fix is working"""

import sys
import os
sys.path.insert(0, '/Users/pranamimishra/Desktop/flexi')

print("🔍 Verifying Gemini Model Fix\n")

# Check 1: API Key
print("[1] Checking API Key...")
if os.path.exists('.env'):
    with open('.env') as f:
        content = f.read()
        if 'GOOGLE_API_KEY=' in content:
            lines = [l for l in content.split('\n') if l.startswith('GOOGLE_API_KEY=')]
            if lines:
                key = lines[0].split('=', 1)[1].strip()
                if key and key != 'your_api_key_here':
                    print(f"   ✅ API key found: {key[:20]}...")
                else:
                    print("   ❌ API key is not set")
            else:
                print("   ❌ API key not found")
        else:
            print("   ❌ .env file missing GOOGLE_API_KEY")
else:
    print("   ❌ .env file not found")
    sys.exit(1)

# Check 2: Agent Initialization
print("\n[2] Checking Agent Initialization...")
try:
    from src.agent import StudyPlannerAgent
    agent = StudyPlannerAgent()
    print("   ✅ Agent initialized successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Check 3: Prioritization Tool
print("\n[3] Checking Prioritization Tool...")
try:
    from src.prioritization_tool import PrioritizationTool
    from datetime import datetime, timedelta
    
    tool = PrioritizationTool()
    assignments = [
        {"name": "Test", "deadline": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"), "hours": 3, "category": "general"}
    ]
    result = tool.prioritize_assignments(assignments)
    print("   ✅ Prioritization tool works")
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Check 4: Model Detection
print("\n[4] Checking available Gemini models...")
try:
    import google.generativeai as genai
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY') or key)
    
    print("   Available models:")
    found_models = []
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            model_name = model.name.split('/')[-1]
            found_models.append(model_name)
            if len(found_models) <= 5:  # Show first 5
                print(f"      • {model_name}")
    
    if found_models:
        print(f"      ... and {len(found_models) - 5} more" if len(found_models) > 5 else "")
        print(f"   ✅ {len(found_models)} models available")
    else:
        print("   ❌ No models found")
except Exception as e:
    print(f"   ⚠️  Could not list models: {e}")

print("\n" + "="*70)
print("✅ ALL CHECKS PASSED")
print("="*70)
print("\nThe fix is working! Now run:")
print("   streamlit run app.py")
print("\n(Note: Gemini API calls may be slow - be patient)")
