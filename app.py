"""
AI Study Planner - Streamlit Web Interface

A user-friendly interface for the Study Planner Agent that:
- Collects assignment information from the user
- Displays prioritized assignments
- Shows the AI-generated study plan
- Handles errors gracefully
"""

import streamlit as st
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from src.agent import StudyPlannerAgent
from src.prioritization_tool import PrioritizationTool

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main {
        max-width: 1200px;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1em;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


def get_agent():
    """Initialize the study planner agent."""
    try:
        return StudyPlannerAgent()
    except ValueError as e:
        st.error(f"❌ Agent initialization error: {str(e)}")
        return None


def validate_api_key():
    """Check if Groq API key is configured."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        st.warning(
            "⚠️ Groq API key not configured. "
            "Please add GROQ_API_KEY to your .env file. "
            "[Get a free API key here](https://console.groq.com/keys)"
        )
        return False
    return True


def display_assignment_form():
    """Render the assignment input form."""
    st.subheader("📝 Enter Your Assignments")
    
    # Input method selection
    input_method = st.radio(
        "How would you like to input assignments?",
        ["Form Entry", "JSON Upload"],
        horizontal=True
    )
    
    assignments = []
    
    if input_method == "Form Entry":
        # Form-based input
        st.info(
            "ℹ️ Add your assignments one by one. "
            "Dates can be in YYYY-MM-DD or DD/MM/YYYY format."
        )
        
        num_assignments = st.number_input(
            "How many assignments do you have?",
            min_value=1,
            max_value=10,
            value=3
        )
        
        for i in range(num_assignments):
            with st.expander(f"Assignment {i + 1}", expanded=(i == 0)):
                col1, col2 = st.columns(2)
                
                with col1:
                    name = st.text_input(
                        f"Assignment name {i + 1}",
                        placeholder="e.g., Math Assignment 1",
                        key=f"name_{i}"
                    )
                    
                    deadline = st.text_input(
                        f"Deadline {i + 1} (YYYY-MM-DD)",
                        value=(datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                        key=f"deadline_{i}"
                    )
                
                with col2:
                    hours = st.number_input(
                        f"Estimated hours {i + 1}",
                        min_value=0.5,
                        max_value=100.0,
                        value=3.0,
                        step=0.5,
                        key=f"hours_{i}"
                    )
                    
                    category = st.selectbox(
                        f"Category {i + 1}",
                        ["general", "project", "exam", "report"],
                        key=f"category_{i}"
                    )
                
                if name and deadline:
                    assignments.append({
                        "name": name,
                        "deadline": deadline,
                        "hours": hours,
                        "category": category
                    })
    
    else:
        # JSON upload
        st.info(
            "📋 Upload JSON file with assignments. "
            "Format: [{\"name\": \"...\", \"deadline\": \"YYYY-MM-DD\", \"hours\": 3, \"category\": \"general\"}, ...]"
        )
        
        uploaded_file = st.file_uploader("Upload JSON file", type="json")
        if uploaded_file:
            try:
                assignments = json.load(uploaded_file)
                st.success(f"✓ Loaded {len(assignments)} assignments")
            except json.JSONDecodeError:
                st.error("Invalid JSON file")
    
    return assignments


def display_available_hours():
    """Get available study hours from user."""
    st.subheader("⏱️ Study Time Available")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        available_hours = st.slider(
            "How many hours can you study per day?",
            min_value=0.5,
            max_value=12.0,
            value=3.0,
            step=0.5,
            help="Total hours available for all subjects combined"
        )
    
    with col2:
        st.metric("Hours/Day", f"{available_hours}h")
    
    return available_hours


def display_results(result):
    """Display agent results in a formatted way."""
    if not result["success"]:
        st.error(f"❌ Error: {result['error']}")
        return
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["Study Plan", "Prioritization Details", "Raw Data"])
    
    with tab1:
        st.subheader("📅 Your Personalized Study Plan")
        st.markdown(result["ai_generated_plan"])
    
    with tab2:
        st.subheader("🎯 Why Assignments Are Prioritized This Way")
        
        # Display as table
        prioritized = result["prioritized_assignments"]
        
        table_data = []
        for idx, item in enumerate(prioritized, 1):
            table_data.append({
                "Priority": idx,
                "Assignment": item["assignment_name"],
                "Days Left": item["days_remaining"],
                "Hours": item["estimated_hours"],
                "Urgency Score": item["urgency_score"],
                "Category": item["category"].capitalize()
            })
        
        st.table(table_data)
        
        st.markdown("---")
        st.subheader("📊 Detailed Breakdown")
        st.text(result["tool_summary"])
    
    with tab3:
        st.subheader("📦 Full Response Data")
        
        # Display as formatted JSON
        display_data = {
            "timestamp": result.get("timestamp"),
            "total_assignments": result.get("total_assignments"),
            "available_hours_per_day": result.get("available_hours_per_day"),
            "prioritized_assignments": result.get("prioritized_assignments"),
        }
        
        st.json(display_data)


def main():
    """Main app logic."""
    # Header
    st.title("📚 AI Study Planner Agent")
    st.markdown(
        "An AI-powered study planning tool that prioritizes your assignments "
        "and creates a personalized study schedule."
    )
    
    st.markdown("---")
    
    # Check API key
    if not validate_api_key():
        st.stop()
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        **Features:**
        - 📋 Assign deadlines and study hours
        - 🤖 AI analyzes priority using urgency score
        - 📅 Creates personalized study plan
        - ⏰ Suggests daily schedules
        
        **How it works:**
        1. Enter your assignments
        2. Set available study hours/day
        3. AI prioritizes and creates plan
        4. View detailed breakdown
        
        **Technologies:**
        - 🐍 Python
        - ⚡ Streamlit
        - 🧠 Groq LLM (Fast & Reliable)
        - 📊 Smart Prioritization
        """)
        
        st.markdown("---")
        st.markdown("*Built for CA3 Agentic AI Course*")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        assignments = display_assignment_form()
    
    with col2:
        available_hours = display_available_hours()
    
    st.markdown("---")
    
    # Generate plan button
    if st.button("🚀 Generate Study Plan", type="primary", use_container_width=True):
        if not assignments:
            st.error("❌ Please add at least one assignment")
            return
        
        with st.spinner("🤔 Analyzing assignments and creating your study plan..."):
            agent = get_agent()
            if agent:
                result = agent.plan_study_schedule(
                    assignments=assignments,
                    available_hours=available_hours
                )
                display_results(result)
                
                # Save result option
                if result["success"]:
                    st.markdown("---")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("💾 Save Plan as JSON"):
                            filename = f"study_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                            
                            save_data = {
                                "timestamp": result["timestamp"],
                                "assignments": assignments,
                                "available_hours": available_hours,
                                "prioritized_assignments": result["prioritized_assignments"],
                                "plan": result["ai_generated_plan"]
                            }
                            
                            with open(f"outputs/{filename}", "w") as f:
                                json.dump(save_data, f, indent=2)
                            
                            st.success(f"✓ Saved to `outputs/{filename}`")
                    
                    with col2:
                        if st.button("📋 Copy Plan to Clipboard"):
                            st.info("Copy the text from the 'Study Plan' tab above")


if __name__ == "__main__":
    main()
