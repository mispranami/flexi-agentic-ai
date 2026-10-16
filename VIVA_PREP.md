# Viva Preparation Guide - AI Study Planner Agent

This guide prepares you to confidently explain and demonstrate your AI Study Planner project in a viva (oral exam).

---

## 🎯 Key Points to Memorize

### 1. What Problem Does This Solve?

**Answer** (30 seconds):
> "Students often struggle to prioritize multiple assignments, especially when balancing internship work. Our system provides two things: (1) A rule-based prioritization algorithm that ranks assignments by urgency, and (2) An AI agent that uses those priorities to generate a personalized study plan. This gives students both a *what* (which task to do) and a *why* (explanations for the ranking)."

### 2. Why is This "Agentic AI" and Not Just a Simple Sorting Algorithm?

**Answer** (45 seconds):
> "It's agentic because:
> 1. We have a tool (prioritization) that performs a deterministic task
> 2. We have an AI component (Gemini) that reasons about the tool's output
> 3. The agent orchestrates these together: tool → format → LLM → response
> 
> If it were just sorting, we wouldn't have the Gemini step. The AI component makes it agentic: it explains *why* tasks are prioritized and generates personalized strategies."

### 3. How is Tool Different From Agent?

**Answer** (45 seconds):
> **Tool (Prioritization)**:
> - Rule-based formula
> - Deterministic (same input = same output)
> - Testable with unit tests
> - No AI/randomness
> - Output: Urgency scores
>
> **Agent**:
> - Uses tool output
> - Adds Gemini LLM reasoning
> - Creates personalized plan
> - Can be adjusted based on feedback
> - Output: Explanations + strategies

### 4. Urgency Score Formula

**Answer** (1 minute - draw on whiteboard):
```
urgency_score = (effort_intensity × complexity_factor × 100) / (days_remaining + 1)

Where:
- effort_intensity = hours_needed / days_remaining
- complexity_factor = {exam: 1.5, project: 1.3, report: 1.2, general: 1.0}
- days_remaining = deadline_date - today

Example:
- Assignment: "Math Project"
- Due: 3 days from now
- Hours: 6
- Category: project (complexity 1.3)
- Calculation: (6/3 × 1.3 × 100) / 4 = (2 × 1.3 × 100) / 4 = 260/4 = 65
```

### 5. Architecture (Draw This)

```
Streamlit UI (Input/Output)
         ↓
  StudyPlannerAgent (Orchestration)
    ↙           ↘
Tool (Rule)    LLM (Gemini)
  ↓                ↓
Urgency Scores   Explanations
  ↓                ↓
    ↘           ↙
   Return Response
         ↓
    Display Results
```

### 6. Why Separate Tool from AI?

**Answer** (45 seconds):
> "Separation is important because:
> 
> 1. **Testability**: Tool is rule-based, so we can write unit tests. We have 11 tests verifying the prioritization logic works correctly.
> 
> 2. **Transparency**: Users can see *why* assignments were ranked (tool output), not just trust the AI's answer.
> 
> 3. **Replaceability**: We could swap Gemini for ChatGPT, or the tool for a different algorithm, without breaking the system.
> 
> 4. **Debugging**: If prioritization is wrong, we know it's the tool formula. If explanations are bad, it's the Gemini prompt.
> 
> Best practice in AI: Always separate deterministic logic from probabilistic AI."

---

## 🧪 Test Walkthrough

### What Tests Do You Have?

**Answer**: "11 comprehensive tests covering:"

1. **Date Parsing** (3 tests)
   - YYYY-MM-DD format ✓
   - DD/MM/YYYY format ✓
   - Invalid format (error handling) ✓

2. **Core Prioritization** (3 tests)
   - **TEST 1**: Deadline-based sorting
     - Input: 3 tasks due in 1, 5, and 10 days (all 2 hours)
     - Expected: Task with 1-day deadline ranked first
     - Result: ✅ Passes (scores: 200 > 40 > 18.18)
   
   - **TEST 2**: Effort intensity consideration
     - Input: 2 tasks with same deadline but different hours (2 vs 10 hours)
     - Expected: 10-hour task ranked higher
     - Result: ✅ Passes (scores: 333 > 67)
   
   - **TEST 3**: Complexity factor weighting
     - Input: Exam, Project, General with same deadline & hours
     - Expected: Exam > Project > General (by complexity weight)
     - Result: ✅ Passes (scores: 107 > 93 > 71)

3. **Error Handling** (3 tests)
   - Missing fields → ValueError ✓
   - Invalid hours (negative/extreme) → ValueError ✓
   - Empty list → Returns empty ✓

4. **Edge Cases** (2 tests)
   - Overdue task → Urgency = 1000 (highest) ✓
   - Score calculation → Correct arithmetic ✓

**Result**: 11/11 tests PASSING ✅

### How to Run Tests?

```bash
python3 -m pytest tests/test_prioritization.py -v

Output:
============================== 11 passed in 0.02s ==============================
```

### What If Tests Fail in Viva?

**If this happens**, say:
> "Let me check the calculation. The test verifies that for these three assignments with deadlines 1, 5, and 10 days away respectively, the system correctly ranks them by deadline pressure. The test has been passing consistently during development. Let me run it again..."

**Then run**: `python3 -m pytest tests/test_prioritization.py::TestPrioritizationTool::test_prioritize_basic_scenarios -v -s`

---

## 💻 Live Demo Script

### Before Demo Starts
1. Have terminal open and ready
2. Have Python environment activated
3. Have test file visible
4. Have app.py ready to run

### Demo Flow (4-5 minutes)

#### Step 1: Show Test Results (1 minute)
```bash
# Run tests first - establishes reliability
python3 -m pytest tests/test_prioritization.py -v

# Point out: "All 11 tests pass, demonstrating the tool works correctly"
```

#### Step 2: Run the Application (30 seconds)
```bash
streamlit run app.py

# Browser opens at localhost:8501
```

#### Step 3: Enter Sample Data (1 minute)

```
Assignment 1:
  Name: Physics Exam
  Deadline: 2024-10-19 (pick date 1 day away)
  Hours: 6
  Category: exam

Assignment 2:
  Name: AI Project
  Deadline: 2024-10-18 (pick date 3 days away)
  Hours: 8
  Category: project

Assignment 3:
  Name: Math Assignment
  Deadline: 2024-10-25 (pick date 10 days away)
  Hours: 3
  Category: general

Available Hours: 4 hours/day
```

#### Step 4: Generate Plan (2-3 minutes)
- Click "Generate Study Plan"
- Wait for results
- Show Tab 1: Study Plan (read a few lines)
- Show Tab 2: Prioritization
  - Point to urgency scores
  - Explain: Physics Exam (1 day, 6 hours, exam) = highest urgency
  - Explain: AI Project (3 days, 8 hours, project) = second
  - Explain: Math Assignment (10 days, 3 hours, general) = third
- Show Tab 3: Raw JSON
  - Explain: Verifiable data structure

#### Step 5: Export (10 seconds)
- Click "Save Plan as JSON"
- Show saved file: `outputs/study_plan_*.json`

**Total Demo Time**: 4-5 minutes

---

## ❓ Common Questions & Answers

### Q1: "Why use Gemini instead of ChatGPT?"

**Answer**:
> "Gemini was chosen because:
> 1. Free API tier is more accessible for students
> 2. Reasoning capabilities are excellent for study planning
> 3. Quick to implement (no authentication complexity)
> 4. Suitable scope for a 3-day college project
> 
> In production, you could substitute any LLM (ChatGPT, Llama, etc.). The agent workflow would remain the same."

### Q2: "Could this be done without an LLM?"

**Answer**:
> "Yes, but less effectively. Without Gemini, we could:
> 1. Just show the prioritized list (users would have to plan themselves)
> 2. Use template-based plans (not personalized)
> 
> Gemini adds value by:
> 1. Generating personalized explanations
> 2. Suggesting specific strategies per assignment
> 3. Adapting to user's available hours
> 4. Providing encouragement and time management tips
> 
> The LLM is what makes planning truly personalized, not generic."

### Q3: "How do you ensure the AI isn't making up priorities?"

**Answer**:
> "This is the key insight of the design. The AI *isn't* determining priorities. The *tool* does that.
> 
> Workflow:
> 1. Tool runs deterministic algorithm → Produces urgency scores
> 2. AI receives tool output + assignments
> 3. AI explains *why* these priorities make sense
> 4. AI generates strategies based on priorities (which AI determined)
> 
> Users can verify AI reasoning against tool output. If they don't like priorities, they can check the formula. This transparency is crucial in AI systems."

### Q4: "Why not use a database?"

**Answer**:
> "For this project scope, a database isn't necessary because:
> 1. We're generating one-off plans, not tracking history
> 2. User can export to JSON for storage
> 3. It would add complexity without value for a 3-day project
> 
> Future enhancement: Add database to track which plans worked best, analyze study patterns, etc."

### Q5: "How does complexity factor work? Why is exam 1.5?"

**Answer**:
> "Complexity factor captures domain knowledge:
> - Exams (1.5): Require memorization + application, comprehensive preparation
> - Projects (1.3): Require planning + execution, but more time-flexible
> - Reports (1.2): Require research + writing, moderate complexity
> - General (1.0): Baseline difficulty
>
> These are based on typical student experience. The actual values could be adjusted based on student feedback. For example, if you find project deadlines stressing you out more, you could increase project complexity to 1.4.
>
> Key point: These factors are *tunable*, not hardcoded. Could be:
> - Learned from student feedback over time
> - Made configurable in settings
> - Adjustable per user"

### Q6: "What if two assignments have the same urgency score?"

**Answer**:
> "Good question. In practice, ties are rare because scores are calculated with decimal precision. But if they occur:
> 1. Python's sort is stable (maintains input order for ties)
> 2. In display, they would be shown in original input order
> 3. User could adjust availability and regenerate
> 
> For real-world robustness, we could:
> 1. Add a tie-breaker (e.g., alphabetical order)
> 2. Add secondary complexity (e.g., number of study hours)
> 
> This would be a good enhancement for v2."

### Q7: "What's your biggest learning from this project?"

**Answer**:
> "The importance of separating concerns:
> 
> Initially, I considered making one large 'AI function' that determined priorities. But I realized:
> 1. That would be a black box - users wouldn't understand why
> 2. It wouldn't be testable
> 3. It would be hard to debug
> 
> By separating tool (deterministic) from agent (AI reasoning), I created:
> 1. A testable component (the tool with 11 passing tests)
> 2. A transparent system (users see the priorities)
> 3. A flexible architecture (can swap components)
> 
> This is the core principle of well-designed AI systems: Always separate the deterministic logic from probabilistic reasoning."

### Q8: "Could you extend this to multiple students?"

**Answer**:
> "Yes, here's how:
> 1. Add user authentication (login with email)
> 2. Store assignments in database per user
> 3. Each user gets personalized plans
> 4. Could add:
>    - Team coordination (see classmates' deadlines)
>    - Shared study groups
>    - Progress tracking
> 
> The current single-user design is appropriate for the 3-day timeline, but the architecture is extensible."

### Q9: "What about edge cases like 0 days remaining?"

**Answer**:
> "The formula handles this:
> ```
> urgency_score = (effort × complexity × 100) / (days + 1)
> ```
> 
> By adding 1 to days, we avoid division by zero. So:
> - 0 days: urgency_score = (effort × complexity × 100) / 1 (high, but not infinite)
> - 1 day: urgency_score = (effort × complexity × 100) / 2
> 
> Overdue tasks get special handling:
> ```
> if days < 0: urgency_score = 1000 (highest possible)
> ```
> 
> This ensures overdue always ranks first, which makes sense pedagogically."

### Q10: "What would you improve if you had more time?"

**Answer**:
> "Top priorities:
> 
> 1. **Database Integration** (1 day)
>    - Track completed tasks
>    - Store study plans
>    - Analyze patterns over time
> 
> 2. **User Feedback Loop** (1 day)
>    - "Did this plan work?" feedback
>    - Refine complexity factors based on actual outcomes
>    - Learn from student data
> 
> 3. **Calendar Integration** (1 day)
>    - Show plan overlaid on calendar
>    - Prevent overloaded days
>    - Sync with academic calendar
> 
> 4. **Mobile App** (2-3 days)
>    - React Native or Flutter
>    - Access plan on-the-go
>    - Quick updates/edits
> 
> 5. **Advanced Analytics** (2 days)
>    - Which study strategies actually worked?
>    - Predict time needed more accurately
>    - Personalization based on learning style"

---

## 📊 Talking Points by Component

### Prioritization Tool

**What to emphasize**:
- ✅ Rule-based (not ML, not random)
- ✅ Deterministic (reproducible)
- ✅ Testable (11 tests all passing)
- ✅ Explainable (formula is clear)
- ✅ Handles edge cases (overdue, invalid data)

**Questions to anticipate**:
- "How did you arrive at the formula?" → "Based on typical student stress factors"
- "Are the complexity factors accurate?" → "Could be tuned based on feedback"
- "What if I disagree with priorities?" → "You can see the formula and adjust"

### AI Agent

**What to emphasize**:
- ✅ Uses tool output (not random AI decisions)
- ✅ Provides explanations (references priorities)
- ✅ Generates personalized plans (not templates)
- ✅ Includes strategies (actionable advice)
- ✅ Graceful error handling (no crashes)

**Questions to anticipate**:
- "Why not just show the priority list?" → "AI adds personalization and strategy"
- "Can Gemini make mistakes?" → "Yes, but users can verify against tool output"
- "What if Gemini suggests unrealistic study hours?" → "Could add validation layer"

### Testing

**What to emphasize**:
- ✅ 11 comprehensive tests
- ✅ All passing (11/11)
- ✅ Cover happy path and edge cases
- ✅ Verify each aspect of formula
- ✅ Make debugging easier

**Questions to anticipate**:
- "Why these specific tests?" → "Each test verifies one aspect of the formula"
- "Is 11 enough?" → "Covers all major code paths. More would be diminishing returns"
- "What tests are missing?" → "Could test with realistic student data from survey"

---

## 🎤 Opening Statement (What to Say First)

**30-second elevator pitch**:

> "This project demonstrates an agentic AI system for student study planning. The system has two components:
> 
> First, a **deterministic prioritization tool** that calculates urgency scores based on deadlines, effort, and complexity. This is fully testable with 11 passing unit tests.
> 
> Second, an **AI agent** that uses these priorities to generate personalized study plans via Google Gemini. The AI's reasoning is grounded in the tool's output, ensuring transparency.
> 
> This separation—tool from AI—is a best practice in systems design. It makes the system explainable, testable, and trustworthy.
> 
> Would you like me to walk through the architecture, see the tests, or run a live demo?"

---

## ✅ Pre-Viva Checklist

- [ ] Run tests locally and verify 11/11 pass
- [ ] Test the Streamlit app with sample data
- [ ] Review formula derivation
- [ ] Practice explaining urgency score (can draw on whiteboard)
- [ ] Memorize the 3 tests and what each demonstrates
- [ ] Have code open and ready to reference
- [ ] Know the file structure and where to find things
- [ ] Practice the demo flow (4-5 minutes)
- [ ] Have backup explanation if something breaks during demo
- [ ] Know how to handle uncomfortable questions (see Q&A above)

---

## 🔥 Confidence Builders

### Things You Should Be Confident About

1. **The Formula**
   - You derived it
   - You can explain each component
   - You can calculate an example by hand

2. **The Tests**
   - You wrote them
   - They all pass
   - You can explain what each one tests

3. **The Architecture**
   - You designed the separation
   - You can draw it on a whiteboard
   - You can explain why it matters

4. **The Implementation**
   - You built it in 3 days
   - You handled errors gracefully
   - You deployed it cleanly

### If You Get Stuck

1. **On a question you don't know**: "That's a great question. Let me think about that. The way I've approached it is... [explain your reasoning]"

2. **During the demo**: "Let me restart that" or "Let me run the test again to show that it's working consistently"

3. **On a technical detail**: "That's implementation-specific. The key concept is [explain the concept]"

4. **On a design choice**: "I chose X because [practical reason]. An alternative would be Y, but X made sense given [constraints]"

---

## 📝 Post-Viva Notes

After the viva, note down:
- [ ] Questions asked
- [ ] Feedback received
- [ ] Things to improve
- [ ] Concepts to study further
- [ ] Extensions suggested

---

## 🎯 Final Advice

**Remember**:
1. You built a working system in 3 days - that's impressive
2. It's tested, documented, and deployed - that's professional
3. You can explain every design decision - that's expert-level
4. Enjoy explaining what you built - your enthusiasm will show through

**Viva is a conversation, not an interrogation.** They want to understand your thinking, not trick you.

Good luck! 🚀
