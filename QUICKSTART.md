# Quick Start - 5 Minutes to Running

**Goal**: Get the AI Study Planner running in 5 minutes flat.

---

## ⚡ 3 Steps

### Step 1: Get Your API Key (2 minutes)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Configure Your Project (1 minute)

```bash
cd flexi
cp .env.template .env
```

Open `.env` and paste your API key:
```
GOOGLE_API_KEY=your_actual_key_here
```

### Step 3: Run the App (2 minutes)

```bash
# Install dependencies (first time only)
pip3 install -r requirements.txt

# Start the app
streamlit run app.py
```

✅ **Done!** Browser opens at http://localhost:8501

---

## 🧪 Verify It's Working

### Run Tests (Optional)
```bash
python3 -m pytest tests/test_prioritization.py -v
# Should see: 11 passed ✅
```

### Run End-to-End Test
```bash
python3 test_e2e.py
# Should see all tests passing ✅
```

---

## 📋 Using the App (1 minute)

1. **Add Assignments**: Fill in name, deadline, hours, category
2. **Set Study Hours**: Pick how many hours/day you can study
3. **Generate Plan**: Click the button
4. **View Results**: 
   - Tab 1: Your personalized study plan
   - Tab 2: Why tasks are prioritized
   - Tab 3: Raw data (JSON)
5. **Export** (optional): Save plan as JSON

---

## ❓ Troubleshooting

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run: `pip3 install -r requirements.txt` |
| `GOOGLE_API_KEY not found` | Check your .env file has the key |
| Streamlit won't start | Check port 8501 is free, or use: `streamlit run app.py --server.port 8502` |
| Tests fail | Ensure you're in the flexi directory |

---

## 📚 Learn More

- **How it works**: See README.md
- **Architecture details**: See ARCHITECTURE.md
- **For your viva**: See VIVA_PREP.md
- **Full submission**: See COLLEGE_SUBMISSION.md

---

**That's it!** 🎉 You're ready to use the AI Study Planner.
