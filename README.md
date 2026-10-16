# AI Study Planner Agent

A beginner-friendly AI-powered study planning application built with Python, Google Gemini, and Streamlit. The application prioritizes assignments based on deadlines and effort, then uses an AI agent to generate personalized study schedules.

**Course:** CA3 Agentic AI  
**Status:** ✅ Complete and Working

---

## 🎯 Project Overview

### Problem
Students often struggle to prioritize multiple assignments, especially when balancing internships and coursework. They need a quick, intelligent way to:
- Identify which assignments are most urgent
- Understand *why* certain tasks matter more
- Get a realistic study schedule based on available time

### Solution
An **AI agent workflow** that:
1. **Receives** assignment details (name, deadline, estimated hours, category)
2. **Uses a prioritization tool** to calculate urgency scores (deterministic, rule-based)
3. **Leverages Gemini LLM** to generate personalized, explanatory study plans
4. **Displays** results in an interactive Streamlit interface

### Key Features
- ✅ Multi-format date input (YYYY-MM-DD, DD/MM/YYYY)
- ✅ Assignment categorization (general, project, exam, report)
- ✅ Urgency scoring based on deadlines, effort, and complexity
- ✅ AI-generated explanations for prioritization
- ✅ Personalized day-by-day study schedule
- ✅ Error handling and input validation
- ✅ JSON export of study plans
- ✅ Responsive Streamlit UI

---

## 🏗️ Architecture

### Component Structure

```
AI Study Planner Agent
│
├── 1. USER INTERFACE (Streamlit)
│   └── app.py
│       ├── Assignment input form
│       ├── Available hours slider
│       └── Results display (tabs: Plan, Details, Data)
│
├── 2. PRIORITIZATION TOOL (Rule-Based)
│   └── src/prioritization_tool.py
│       ├── Date parsing
│       ├── Urgency score calculation
│       └── Assignment ranking algorithm
│
├── 3. AI AGENT (LangGraph + Gemini)
│   └── src/agent.py
│       ├── Tool orchestration
│       ├── Gemini API integration
│       └── Study plan generation
│
└── 4. TESTING
    └── tests/test_prioritization.py
        └── 11 comprehensive unit tests
```

### Data Flow

```
User Input
    ↓
Streamlit UI (app.py)
    ↓
StudyPlannerAgent.plan_study_schedule()
    ↓
┌─────────────────────────────────────┐
│ Prioritization Tool                  │
│ (Calculate Urgency Scores)           │
│ - Parse dates                        │
│ - Calculate days remaining           │
│ - Calculate effort intensity         │
│ - Apply complexity factors           │
│ - Rank assignments                   │
└─────────────────────────────────────┘
    ↓
Google Gemini LLM
    ├─ Input: Assignment list + priorities + tool output
    ├─ Prompt: Create personalized study plan
    └─ Output: Detailed plan with explanations
    ↓
Results Display
├─ Prioritized assignments (table)
├─ AI-generated study plan
└─ JSON export option
```

### Urgency Score Formula

```
If deadline is overdue:
    urgency_score = 1000

Else:
    effort_intensity = estimated_hours / max(days_remaining, 1)
    urgency_score = (effort_intensity × complexity_factor × 100) / (days_remaining + 1)

Higher score = More urgent
```

**Complexity Factors:**
- Exam: 1.5 (most complex)
- Project: 1.3
- Report: 1.2
- General: 1.0 (baseline)

---

## 📋 Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Interface** | Streamlit 1.28+ | Web UI for user interaction |
| **LLM** | Google Gemini Pro | Generate personalized study plans |
| **Framework** | Python 3.9+ | Core application logic |
| **Orchestration** | Langgraph | Agent workflow (optional—can run without) |
| **Config** | python-dotenv | Secure API key management |
| **Testing** | pytest | Unit tests for prioritization logic |

### Why These Technologies?

1. **Streamlit**: Zero-config web app deployment, perfect for beginners
2. **Google Gemini**: Free API tier, excellent reasoning for study planning
3. **Python**: Easy to understand, great for beginners
4. **pytest**: Standard testing framework with clear syntax

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9 or higher
- Google Gemini API key (free: https://makersuite.google.com/app/apikey)
- Terminal/Command prompt

### 2. Installation

```bash
# Clone or download the project
cd flexi

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API key
# .env
# GOOGLE_API_KEY=your_actual_api_key_here
```

### 4. Run the Application

```bash
# Start Streamlit app (opens in browser at http://localhost:8501)
streamlit run app.py
```

### 5. Using the App

1. **Enter Assignments**: Add assignment name, deadline, hours, and category
2. **Set Study Hours**: Specify available hours per day
3. **Generate Plan**: Click "🚀 Generate Study Plan"
4. **View Results**: See prioritization rationale and personalized schedule
5. **Export**: Save plan as JSON (optional)

---

## 🧪 Running Tests

```bash
# Run all tests
python3 -m pytest tests/ -v

# Run with output (see print statements)
python3 -m pytest tests/test_prioritization.py -v -s

# Run specific test
python3 -m pytest tests/test_prioritization.py::TestPrioritizationTool::test_prioritize_basic_scenarios -v
```

### Test Coverage

**11 tests total covering:**
- ✅ Date parsing (YYYY-MM-DD, DD/MM/YYYY formats)
- ✅ Basic prioritization (deadline-based sorting)
- ✅ Effort intensity consideration (same deadline, different hours)
- ✅ Complexity factor application (exam vs project vs general)
- ✅ Error handling (missing fields, invalid values)
- ✅ Edge cases (empty lists, overdue tasks, extreme values)
- ✅ Urgency score calculation accuracy

**All tests pass:** ✅ 11/11 PASSING

---

## 📁 Project Structure

```
flexi/
├── app.py                          # Streamlit web interface (main entry point)
├── requirements.txt                # Python dependencies
├── .env.template                   # API key template (copy to .env)
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
│
├── src/
│   ├── __init__.py
│   ├── prioritization_tool.py      # Rule-based prioritization (240 lines)
│   └── agent.py                    # LangGraph + Gemini integration (180 lines)
│
├── tests/
│   ├── __init__.py
│   └── test_prioritization.py      # Unit tests (220 lines, 11 tests)
│
└── outputs/
    └── study_plan_*.json           # Exported study plans (generated)
```

### File Descriptions

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 350 | Streamlit UI: forms, results display, export |
| `src/prioritization_tool.py` | 240 | Urgency scoring, date parsing, sorting algorithm |
| `src/agent.py` | 180 | Agent workflow, Gemini integration, prompt engineering |
| `tests/test_prioritization.py` | 220 | 11 comprehensive unit tests |

---

## 🔑 Key Code Sections

### Prioritization Tool (Deterministic)

```python
# Not AI - rule-based algorithm
urgency_score = (effort_intensity × complexity_factor × 100) / (days_remaining + 1)

# Higher effort + shorter deadline = higher urgency
# Exams weighted higher than general tasks
```

### Agent Workflow (AI Component)

```python
def plan_study_schedule(assignments, available_hours):
    # Step 1: Validate inputs
    # Step 2: Call prioritization tool (deterministic)
    prioritized = tool.prioritize_assignments(assignments)
    
    # Step 3: Create context with tool output
    context = format_for_gemini(prioritized, available_hours)
    
    # Step 4: Ask Gemini to create plan (AI reasoning)
    response = gemini.generate_content(context)
    
    # Step 5: Return structured response
    return formatted_response
```

### Separation of Concerns

- **Tool (src/prioritization_tool.py)**: Deterministic, reproducible, testable
- **Agent (src/agent.py)**: Uses tool output + AI reasoning for explanations
- **UI (app.py)**: Orchestrates and displays results

---

## ⚙️ Configuration Options

### Environment Variables

```bash
# .env file (REQUIRED)
GOOGLE_API_KEY=your_api_key_here
```

### Streamlit Settings

Edit `~/.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#3498db"
backgroundColor = "#2c3e50"
secondaryBackgroundColor = "#34495e"
textColor = "#ecf0f1"
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `GOOGLE_API_KEY not found` | Copy `.env.template` to `.env` and add your key |
| `ModuleNotFoundError: No module named 'streamlit'` | Run `pip install -r requirements.txt` |
| Tests fail locally | Ensure Python 3.9+, run from project root |
| Streamlit won't start | Check port 8501 is free, try `streamlit run app.py --server.port 8502` |
| API quota exceeded | Free tier has usage limits; wait or upgrade |
| Date parsing errors | Use YYYY-MM-DD or DD/MM/YYYY format exactly |

---

## 🎓 Learning Outcomes

By reviewing this project, you'll understand:

1. **Agentic AI Pattern**: How to separate rule-based tools from AI reasoning
2. **LLM Integration**: Using Google Gemini API for natural language reasoning
3. **Python Best Practices**: Clean code, error handling, testing
4. **Prompt Engineering**: Writing effective prompts for AI agents
5. **Full-Stack Development**: UI → Logic → Testing workflow

---

## 📊 Performance & Scalability

- **Typical response time**: 2-3 seconds (API call included)
- **Max assignments**: Tested up to 20 (no hard limit)
- **Cost**: Free tier (Gemini API offers free quota)
- **Hosting**: Can deploy to Streamlit Cloud for free

---

## 🤝 Support & Contributions

### Getting Help
1. Check the troubleshooting section above
2. Review test examples in `tests/test_prioritization.py`
3. Check Streamlit docs: https://docs.streamlit.io
4. Google Gemini API docs: https://ai.google.dev/docs

### Extending the Project
- Add more assignment categories
- Implement multi-week planning
- Add calendar integration
- Store plans in a database
- Add user authentication

---

## 📄 License

This is a college project. Use freely for educational purposes.

---

## 📝 Credits

**Course:** CA3 Agentic AI  
**Built by:** [Your Name]  
**Date:** October 2024  
**Frameworks:** Streamlit, Google Gemini, Python

---

## ✅ Checklist for College Submission

- [x] Setup instructions (see Quick Start)
- [x] Code documentation (docstrings throughout)
- [x] Unit tests (11 tests, all passing)
- [x] Error handling (input validation, API errors)
- [x] README with architecture explanation
- [x] Technology justification (see Technology Stack)
- [x] Separated tool from AI agent
- [x] Clear separation of concerns
- [ ] Viva prep notes (see `COLLEGE_SUBMISSION/viva_prep.md`)
- [ ] Architecture diagram (see `COLLEGE_SUBMISSION/ARCHITECTURE.md`)

---

## 🚀 Next Steps

1. **Set up API key**: Add your Gemini API key to `.env`
2. **Run tests**: Verify everything works with `pytest tests/ -v`
3. **Start the app**: Run `streamlit run app.py`
4. **Test the workflow**: Enter sample assignments and generate a plan
5. **Review output**: Check the college submission documents

Happy studying! 📚
