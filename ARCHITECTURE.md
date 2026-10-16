# AI Study Planner Agent - Architecture Documentation

## System Architecture Overview

```
╔════════════════════════════════════════════════════════════════════╗
║                    AI STUDY PLANNER SYSTEM                         ║
╚════════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER (UI)                            │
│                                                                     │
│  app.py - Streamlit Interface                                      │
│  ├─ Assignment Input Form                                          │
│  ├─ Date/Hours Pickers                                             │
│  ├─ Results Display (Tabs)                                         │
│  │  ├─ Tab 1: AI Study Plan                                        │
│  │  ├─ Tab 2: Prioritization Analysis                              │
│  │  └─ Tab 3: Raw JSON Data                                        │
│  └─ Export Functionality                                            │
└────────────────────┬────────────────────────────────────────────────┘
                     │
                     │ User Input: Assignments + Hours
                     │
┌────────────────────▼────────────────────────────────────────────────┐
│                  APPLICATION LAYER                                  │
│                                                                     │
│  StudyPlannerAgent (src/agent.py)                                  │
│  ├─ Input Validation                                               │
│  │  ├─ API key check                                               │
│  │  ├─ Hours range validation (0-24)                               │
│  │  └─ Assignment list check                                       │
│  │                                                                 │
│  ├─ Workflow Orchestration                                         │
│  │  ├─ Step 1: Call Prioritization Tool                            │
│  │  ├─ Step 2: Format for Gemini                                   │
│  │  ├─ Step 3: Call Gemini API                                     │
│  │  └─ Step 4: Package Response                                    │
│  │                                                                 │
│  └─ Error Handling                                                 │
│     ├─ Validation errors                                           │
│     ├─ API errors                                                  │
│     └─ Data parsing errors                                         │
└────────────────────┬────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        │ Tool Results            │ Prompt + Context
        │                         │
┌───────▼──────────┐      ┌──────▼──────────────────┐
│   TOOL LAYER     │      │   AI REASONING LAYER    │
│                  │      │                        │
│ Prioritization   │      │ Google Gemini LLM      │
│ Tool             │      │                        │
│ (Rule-Based)     │      │ ├─ Parse context      │
│                  │      │ ├─ Generate plan      │
│ src/priorit...   │      │ ├─ Explain reasoning  │
│ ization_tool.py  │      │ └─ Format response    │
│                  │      │                        │
│ ├─ Parse Dates   │      │ API Endpoint:         │
│ ├─ Calculate     │      │ https://api.google... │
│ │  Urgency       │      │                        │
│ ├─ Sort by       │      │ Model: gemini-pro     │
│ │  Score         │      │                        │
│ └─ Error         │      └────────────────────────┘
│    Handling      │
│                  │
│ Output:          │
│ {                │
│   urgency_score, │
│   days_remaining,│
│   complexity,    │
│   ...            │
│ }                │
└──────────────────┘
```

## Detailed Component Breakdown

### 1. USER INTERFACE (app.py)

**Purpose**: Provide user-friendly interface for assignment entry and result visualization

**Components**:

```python
class StreamlitUI:
    
    def display_assignment_form():
        # Two input methods:
        # 1. Form Entry: Expandable fields (default 3)
        # 2. JSON Upload: Bulk import
        #
        # Fields per assignment:
        # - name: str (required)
        # - deadline: str (YYYY-MM-DD or DD/MM/YYYY)
        # - hours: float (0.5 - 100)
        # - category: select (general, project, exam, report)
        
    def display_available_hours():
        # Slider: 0.5 - 12 hours/day
        # Shows metric display
        
    def display_results():
        # Tab 1: AI Study Plan
        #   - Generated text from Gemini
        #   - Long-form explanations
        #
        # Tab 2: Prioritization Details
        #   - Table of assignments
        #   - Urgency scores
        #   - Detailed breakdown
        #
        # Tab 3: Raw Data
        #   - JSON formatted
        #   - Complete response object
        
    def handle_export():
        # Export to JSON file
        # Filename: study_plan_YYYYMMDD_HHMMSS.json
        # Location: outputs/
```

**Key Features**:
- Input validation at UI level
- Helpful error messages
- Progress spinners during API calls
- Responsive design with st.columns()
- Tab-based result display
- Export with timestamp

**State Management**:
- Streamlit's @st.cache_resource for agent initialization
- Session state for form inputs
- File upload handling

### 2. PRIORITIZATION TOOL (src/prioritization_tool.py)

**Purpose**: Deterministic algorithm for calculating assignment urgency

**Class Hierarchy**:

```python
@dataclass
class Assignment:
    name: str
    deadline_date: str        # YYYY-MM-DD or DD/MM/YYYY
    estimated_hours: float
    category: str            # general, project, exam, report

class PrioritizationTool:
    
    def __init__(available_hours_per_day=3.0):
        # Store available hours for context
        
    def parse_date(date_str: str) -> datetime:
        # Try YYYY-MM-DD first
        # Try DD/MM/YYYY second
        # Raise ValueError if both fail
        # Strips whitespace for robustness
        
    def calculate_urgency_score(assignment: Assignment) -> Dict:
        # Calculate days_remaining = deadline - today
        # Get complexity_factor based on category
        # Calculate effort_intensity = hours / days_remaining
        # Apply formula: (effort × complexity × 100) / (days + 1)
        # Special case: overdue → score = 1000
        #
        # Returns breakdown with all components
        
    def prioritize_assignments(assignments: List[Dict]) -> List[Dict]:
        # Validate all assignments
        # Convert to Assignment objects
        # Calculate scores for each
        # Sort descending by score
        # Return annotated list
```

**Urgency Score Formula**:

```
days_remaining = deadline_date - today

If days_remaining < 0:
    urgency_score = 1000  # Overdue gets highest score

Else:
    complexity_factor = {
        'exam': 1.5,
        'project': 1.3,
        'report': 1.2,
        'general': 1.0
    }
    
    effort_intensity = estimated_hours / max(days_remaining, 1)
    
    urgency_score = (effort_intensity × complexity_factor × 100) / (days_remaining + 1)
```

**Example Calculation**:

```
Assignment: "Math Project"
- Deadline: 3 days from now
- Hours needed: 6
- Category: project (complexity = 1.3)

Calculation:
- days_remaining = 3
- effort_intensity = 6 / 3 = 2.0
- urgency_score = (2.0 × 1.3 × 100) / (3 + 1)
                = 260 / 4
                = 65

Higher score → More urgent
```

**Why This Formula?**

| Component | Effect | Reasoning |
|-----------|--------|-----------|
| `estimated_hours / days_remaining` | Captures pressure | Fewer days, more hours = higher stress |
| `complexity_factor` | Domain knowledge | Exams inherently harder than general tasks |
| `× 100` | Scaling | Makes scores readable (not decimals) |
| `/ (days_remaining + 1)` | Normalization | Prevents division by zero, weights urgency |

**Error Handling**:

```python
ValidationError scenarios:
- Missing required field (name, deadline, hours)
  → ValueError: "Assignment X missing required fields"
  
- Invalid date format
  → ValueError: "Invalid date format. Use YYYY-MM-DD or DD/MM/YYYY"
  
- Negative hours
  → ValueError: "Hours cannot be negative"
  
- Hours > 100
  → ValueError: "Hours seems too high"
  
- Non-numeric hours
  → ValueError: "Hours must be numeric"
```

**Output Structure**:

```python
{
    "assignment_name": "Math Project",
    "days_remaining": 3,
    "estimated_hours": 6,
    "complexity_factor": 1.3,
    "effort_intensity": 2.0,
    "urgency_score": 65.0,
    "category": "project"
}
```

### 3. AI AGENT (src/agent.py)

**Purpose**: Orchestrate workflow combining tool + LLM reasoning

**Class Structure**:

```python
class StudyPlannerAgent:
    
    def __init__(api_key=None):
        # Load API key from .env or parameter
        # Configure Gemini
        # Initialize PrioritizationTool
        
    def plan_study_schedule(
        assignments: List[Dict],
        available_hours: float = 3.0
    ) -> Dict:
        """
        Main workflow:
        
        Step 1: Validate
        ├─ Check API key
        ├─ Check hours in range (0-24)
        └─ Check assignments not empty
        
        Step 2: Prioritize (call tool)
        ├─ Pass to PrioritizationTool
        └─ Get urgency-ranked list
        
        Step 3: Format for Gemini
        ├─ Create detailed prompt
        ├─ Include tool output
        ├─ Specify format requirements
        └─ Add context about available hours
        
        Step 4: Call Gemini
        ├─ Send prompt
        ├─ Get response
        └─ Extract text
        
        Step 5: Return Structured Response
        ├─ success: boolean
        ├─ timestamp: ISO format
        ├─ prioritized_assignments: list
        ├─ tool_summary: human-readable
        ├─ ai_generated_plan: study plan
        └─ error: null if success
        """
        
    def plan_study_schedule_with_feedback(
        assignments,
        available_hours,
        user_feedback=None
    ) -> Dict:
        # Get initial plan
        # If user_feedback provided:
        #   ├─ Create refinement prompt
        #   ├─ Call Gemini again
        #   └─ Return updated plan
```

**Workflow Diagram**:

```
Input: assignments, available_hours
  │
  ├─ Is API key set? ──NO──> Error: "API key not found"
  │
  ├─ Is hours in (0, 24)? ──NO──> Error: "Invalid hours"
  │
  ├─ Has assignments? ──NO──> Error: "No assignments"
  │
  └─ YES to all ──> Call PrioritizationTool
                         │
                         ├─ Parse dates
                         ├─ Calculate scores
                         └─ Sort by urgency
                              │
                              └─ Get prioritized list
                                   │
                                   ├─ Create context
                                   ├─ Format prompt
                                   └─ Call Gemini
                                        │
                                        ├─ API call
                                        ├─ Get response
                                        └─ Extract text
                                             │
                                             └─ Package response
                                                  └─ Return to UI
```

**Prompt Engineering**:

The prompt sent to Gemini includes:

1. **Context Setting**
   ```
   "You are an expert study planning assistant."
   "A student has provided assignments and available study time."
   ```

2. **Data Provided**
   - Available study hours/day
   - Full assignment list
   - Prioritization analysis (from tool)
   - Urgency scores

3. **Task Definition**
   ```
   Review the prioritized list.
   Create a DETAILED, PERSONALIZED study plan that:
   - Explains WHY each assignment is prioritized
   - References urgency scores
   - Allocates study time from available hours/day
   - Provides specific strategies
   - Suggests which days for which assignments
   - Gives actionable time management tips
   ```

4. **Format Requirements**
   - Clear summary (2-3 sentences)
   - Prioritization reasoning
   - Day-by-day breakdown
   - Specific strategies per assignment
   - Tips for staying on track

**Key Principle**: Tool output is ALWAYS included in Gemini's context
- User can verify AI reasoning against tool output
- AI explains *why* priorities matter
- System is transparent and auditable

### 4. TESTING LAYER (tests/test_prioritization.py)

**Test Categories**:

```
11 Total Tests
├─ Date Parsing (3 tests)
│  ├─ YYYY-MM-DD format
│  ├─ DD/MM/YYYY format
│  └─ Invalid format (error)
│
├─ Core Prioritization (3 tests)
│  ├─ TEST 1: Deadline-based sorting
│  ├─ TEST 2: Effort intensity consideration
│  └─ TEST 3: Complexity factor weighting
│
├─ Error Handling (3 tests)
│  ├─ Missing required fields
│  ├─ Invalid hours (negative/extreme)
│  └─ Empty assignment list
│
└─ Edge Cases (2 tests)
   ├─ Overdue assignments
   └─ Urgency score calculation
```

**Test Structure**:

```python
class TestPrioritizationTool:
    def setup_method(self):
        # Create fresh tool instance
        self.tool = PrioritizationTool(available_hours_per_day=3.0)
    
    def test_basic_scenario(self):
        # Arrange: Create test data
        assignments = [...]
        
        # Act: Call function
        result = self.tool.prioritize_assignments(assignments)
        
        # Assert: Verify results
        assert result[0]["assignment_name"] == "Expected"
        assert result[0]["urgency_score"] > result[1]["urgency_score"]
        
        # Document: Print result
        print("✓ TEST PASSED: ...")
```

**Each Test Demonstrates**:

| Test | Demonstrates |
|------|---------------|
| TEST 1 | Shorter deadline = higher priority |
| TEST 2 | More effort + same deadline = higher priority |
| TEST 3 | Same deadline/hours but exam > project > general |
| Error tests | Graceful failure with helpful messages |
| Edge cases | System robustness |

## Data Flow Architecture

### Request Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER SUBMITS FORM                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │ Assignment   │  │ Assignment   │  │ Available    │           │
│  │ Name: String │  │ Deadline: Str│  │ Hours: Float │           │
│  │ Hours: Float │  │ Category: Str│  │              │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ JSON Payload
                     │
┌────────────────────▼────────────────────────────────────────────┐
│              STREAMLIT VALIDATION                                │
│  ├─ Number of assignments?                                      │
│  ├─ All fields filled?                                          │
│  └─ Types correct?                                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Valid? → YES
                     │
┌────────────────────▼────────────────────────────────────────────┐
│         CALL agent.plan_study_schedule()                        │
└────────────────────┬────────────────────────────────────────────┘
                     │
    ┌────────────────┴────────────────┐
    │                                 │
    │ Input Validation                │ Prioritization Tool
    │ ├─ API key?                    │ ├─ Parse dates
    │ ├─ Hours valid?                │ ├─ Calculate scores
    │ └─ Assignments exist?          │ └─ Sort by urgency
    │                                 │
    └────────────────┬────────────────┘
                     │
                     │ Tool output + Formatted Prompt
                     │
┌────────────────────▼────────────────────────────────────────────┐
│            CALL Gemini API                                      │
│  ├─ HTTP POST to Google API                                    │
│  ├─ Include: assignments, priorities, context                  │
│  └─ Receive: Generated study plan text                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Response
                     │
┌────────────────────▼────────────────────────────────────────────┐
│         PACKAGE RESPONSE                                        │
│  {                                                              │
│    "success": true,                                             │
│    "timestamp": "2024-10-15T14:30:00",                         │
│    "prioritized_assignments": [...],                           │
│    "tool_summary": "human-readable breakdown",                 │
│    "ai_generated_plan": "detailed study plan text",            │
│    "error": null                                                │
│  }                                                              │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     │ Response Object
                     │
┌────────────────────▼────────────────────────────────────────────┐
│           DISPLAY RESULTS                                       │
│  ├─ Tab 1: AI Plan (markdown)                                  │
│  ├─ Tab 2: Details (table + summary)                           │
│  ├─ Tab 3: Raw Data (JSON)                                     │
│  └─ Export Option                                              │
└────────────────────────────────────────────────────────────────┘
```

### Response Object Structure

```json
{
  "success": true,
  "error": null,
  "timestamp": "2024-10-15T14:30:45.123456",
  "available_hours_per_day": 4.0,
  "total_assignments": 3,
  
  "prioritized_assignments": [
    {
      "assignment_name": "Physics Exam",
      "days_remaining": 1,
      "estimated_hours": 6,
      "complexity_factor": 1.5,
      "effort_intensity": 6.0,
      "urgency_score": 450.0,
      "category": "exam"
    },
    ...
  ],
  
  "tool_summary": "📋 PRIORITIZED ASSIGNMENTS:\n...",
  
  "ai_generated_plan": "Based on your assignments and available study time..."
}
```

## Error Handling Architecture

### Error Categories

```
Errors
├─ Configuration Errors
│  ├─ Missing API key
│  └─ Invalid API key format
│
├─ Validation Errors
│  ├─ Invalid hours (not 0-24)
│  ├─ Empty assignment list
│  ├─ Missing required fields
│  ├─ Invalid date format
│  └─ Invalid field types
│
├─ Data Errors
│  ├─ Negative hours
│  ├─ Unrealistically high hours
│  └─ Empty assignment names
│
├─ API Errors
│  ├─ Network timeout
│  ├─ Rate limit exceeded
│  ├─ Invalid API response
│  └─ Gemini service unavailable
│
└─ System Errors
   ├─ Unexpected exceptions
   └─ System-level failures
```

### Error Handling Strategy

```
TRY
├─ Validate API key exists
├─ Validate hours in range
├─ Validate assignments exist
├─ Call prioritization tool
│  ├─ TRY validate each assignment
│  ├─ TRY parse dates
│  └─ CATCH and return specific error
├─ Call Gemini API
│  ├─ TRY make request
│  ├─ TRY parse response
│  └─ CATCH API errors
└─ Return structured response

CATCH all exceptions
├─ Log error details
├─ Return error response with helpful message
└─ Ensure app doesn't crash
```

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Reasoning |
|-----------|-----------|-----------|
| Parse single date | O(1) | Regex + string parsing |
| Calculate single score | O(1) | Simple arithmetic |
| Prioritize N assignments | O(N log N) | Sorting operation |
| Validate N assignments | O(N) | Linear scan |
| Format for display | O(N) | Linear scan |

### Space Complexity

| Component | Space | Reasoning |
|-----------|-------|-----------|
| Priority scores | O(N) | One score per assignment |
| Tool output | O(N) | All assignments + metadata |
| Response object | O(N + M) | N = assignments, M = plan text |
| Agent state | O(1) | Single agent instance |

### Typical Performance

```
Scenario: 5 assignments
├─ UI input validation: < 10ms
├─ Prioritization tool: < 5ms
├─ Prompt formatting: < 10ms
├─ Gemini API call: 2-3 seconds
└─ Response formatting: < 50ms

Total: ~2-3 seconds (dominated by API)
```

### Scalability

| Metric | Limit | Impact |
|--------|-------|--------|
| Assignments | 100+ | No technical limit, UI may become cluttered |
| API calls/day | 60 (free tier) | Adequate for personal use |
| Response size | ~10KB | Small enough for any network |
| Database | Not used | No storage bottlenecks |

## Security Considerations

### API Key Protection

```
.env file contains: GOOGLE_API_KEY=***
├─ Added to .gitignore (never committed)
├─ Loaded at runtime via python-dotenv
├─ Not exposed in logs
└─ Not hardcoded in source
```

### Input Validation

```
All user inputs validated before processing:
├─ Assignment names: string, not empty
├─ Dates: parsed and validated format
├─ Hours: float, in realistic range
├─ Categories: whitelisted values
└─ Hours available: numeric, in range
```

### API Security

```
Gemini API calls:
├─ Use official SDK (google-generativeai)
├─ HTTPS only (automatic)
├─ API key never exposed to client
└─ No sensitive data in prompts
```

## Extension Points

### How to Extend

```
1. Add new prioritization strategy
   ├─ Subclass PrioritizationTool
   ├─ Override calculate_urgency_score()
   └─ Agent automatically uses new logic

2. Add new LLM
   ├─ Update agent.py __init__()
   ├─ Change API call
   └─ Adjust prompt format

3. Add new UI features
   ├─ Update app.py
   ├─ Add new Streamlit components
   └─ No changes needed to logic

4. Add persistence
   ├─ Update agent to save to DB
   ├─ Create database schema
   └─ Query historical plans
```

### Maintained Separation

All extensions maintain:
- ✅ Tool = Deterministic, testable
- ✅ Agent = Uses tool + AI reasoning
- ✅ UI = Orchestrates components
- ✅ Tests = Cover new logic

---

## Summary

This architecture ensures:

1. **Modularity**: Each layer has single responsibility
2. **Testability**: Tool logic is isolated and testable
3. **Transparency**: Tool output always visible
4. **Maintainability**: Clear data flow, well-documented
5. **Scalability**: Can extend without breaking existing code
6. **Reliability**: Comprehensive error handling
7. **Security**: API keys protected, inputs validated

The design clearly separates rule-based tool (deterministic) from AI reasoning (probabilistic), making the system both explainable and intelligent.
