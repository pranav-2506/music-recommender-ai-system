# Interactive Testing Guide - Music Recommender AI System

This guide walks you through testing the interactive mode with your free Gemini API key.

---

## Step 1: Get Your Free Gemini API Key (5 minutes)

### 1.1 Navigate to Google AI Studio

Go to: **[https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)**

### 1.2 Click "Create API Key"

You'll see a button that says:
- **"Create API Key in new Google Cloud project"** (first time), OR
- **"Create API Key"** (if you already have a project)

Click it.

### 1.3 Copy Your API Key

A dialog will appear with your new API key:
```
AIzaSyD...your_actual_key_here...
```

**⚠️ Important:**
- Copy the ENTIRE key (it's long, like 50+ characters)
- Don't share this key publicly
- Paste it exactly into your `.env` file

---

## Step 2: Configure Your .env File (2 minutes)

### 2.1 Create .env from template

```bash
cd /Users/pranavchandar/Desktop/2026/Spring\ 2026/codpath/music-recommender-ai-system
cp .env.example .env
```

### 2.2 Edit .env and add your key

```bash
# Open in your editor of choice
nano .env
# or: vim .env
# or: code .env  (if using VS Code)
```

**Your .env should look like:**
```
GOOGLE_API_KEY=AIzaSyD_1234567890abcdefghijklmnopqrstuvwxyz
```

(Replace with your actual key)

### 2.3 Save and close

If using nano: `Ctrl+X`, then `Y`, then `Enter`

### 2.4 Verify it worked

```bash
# Check the file was saved correctly
cat .env
# Should print: GOOGLE_API_KEY=AIzaSyD_...
```

---

## Step 3: Activate Virtual Environment & Install Dependencies (2 minutes)

```bash
# From the project root
source ../.venv/bin/activate

# You should see (.venv) at the start of your prompt
# (or use .venv\Scripts\activate on Windows)
```

### 3.1 Install Requirements

```bash
# Install all dependencies (google-generativeai, python-dotenv, etc.)
pip install -r requirements.txt
```

You should see output like:
```
Installing collected packages: google-generativeai, python-dotenv, ...
Successfully installed ...
```

---

## Step 4: Run Interactive Mode (5 minutes)

### 4.1 Start the system

```bash
python3 -m src.main
```

You should see:

```
🎵 Music Recommender AI System
========================================================
Describe the music you're in the mood for (type 'quit' to exit):

>
```

### 4.2 Try Test Input #1: Simple Request

Type:
```
> something chill for studying
```

Press Enter and **watch what happens**:

```
[Agent Step 1] Parsing user intent with Gemini...
  Extracted prefs: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35}
[Agent Step 2] Retrieving context for lofi/chill...
  Retrieved 340 chars of context.
[Agent Step 3] Scoring and ranking songs...
  Ranked 5 unique songs.
[Agent Step 4] Generating explanation with Gemini...
  Explanation generated.
[Agent Step 5] Validating recommendations...
  Confidence: 0.86 ✓

✨ Top Recommendations:

  1. Library Rain — Paper Lanterns
     Genre: lofi | Mood: chill | Score: 9.00

  2. Midnight Coding — LoRoom
     Genre: lofi | Mood: focused | Score: 8.71

  3. Focus Flow — LoRoom
     Genre: lofi | Mood: focused | Score: 8.50

  4. Spacewalk Thoughts — Orbit Bloom
     Genre: ambient | Mood: chill | Score: 7.19

  5. Daydream Static — Pastel Drive
     Genre: dream pop | Mood: dreamy | Score: 6.65

💭 Why: These recommendations combine lo-fi and ambient tracks with high acousticness 
(natural, organic instrumentation) and slower tempos (around 70-80 BPM). Perfect for 
a focused, calm studying environment without distracting vocals or sudden intensity.

📊 Confidence: 86%

============================================================
```

**What to observe:**
- ✅ All 5 steps execute (Parse → Retrieve → Score → Explain → Validate)
- ✅ Top songs are lofi/chill (correct match)
- ✅ Confidence is high (0.86 = 86%)
- ✅ Explanation mentions "acousticness" and "tempos" (using RAG context)

---

### 4.3 Try Test Input #2: High-Energy Request

Type:
```
> pump me up with intense workout music
```

Expected behavior:

```
[Agent Step 1] Parsing user intent with Gemini...
  Extracted prefs: {'genre': 'rock', 'mood': 'intense', 'energy': 0.92}
[Agent Step 2] Retrieving context for rock/intense...
  Retrieved 380 chars of context.
[Agent Step 3] Scoring and ranking songs...
  Ranked 5 unique songs.
[Agent Step 4] Generating explanation with Gemini...
  Explanation generated.
[Agent Step 5] Validating recommendations...
  Confidence: 0.91 ✓

✨ Top Recommendations:

  1. Storm Runner — Voltline
     Genre: rock | Mood: intense | Score: 8.81

  2. Gym Hero — Max Pulse
     Genre: pop | Mood: intense | Score: 6.05

  [... 3 more ...]

💭 Why: These recommendations prioritize high energy and intense mood that drive 
motivation and physical performance. Rock and pop tracks with strong drums and 
driving rhythm create the adrenaline boost you need for a workout.

📊 Confidence: 91%
```

**What to observe:**
- ✅ Top song is rock/intense (correct)
- ✅ High confidence (0.91)
- ✅ Explanation mentions "energy" and "drums"

---

### 4.4 Try Test Input #3: Edge Case (Conflicting Preferences)

Type:
```
> I want sad, melancholic music but also super energetic
```

Expected behavior (watch what happens with conflicting preferences):

```
[Agent Step 1] Parsing user intent with Gemini...
  Extracted prefs: {'genre': 'blues', 'mood': 'sad', 'energy': 0.95}
[Agent Step 2] Retrieving context for blues/sad...
  Retrieved 320 chars of context.
[Agent Step 3] Scoring and ranking songs...
  Ranked 5 unique songs.
[Agent Step 4] Generating explanation with Gemini...
  Explanation generated.
[Agent Step 5] Validating recommendations...
  Confidence: 0.42 ⚠️
  ⚠️  Low confidence (< 0.5): top result scored below 50% of max. Recommendations may be weak matches.

✨ Top Recommendations:

  1. Blue Smoke — Marcus Wells
     Genre: blues | Mood: sad | Score: 5.79

  [... remaining songs ...]

💭 Why: These selections balance melancholic and introspective tones, though they 
lean toward lower energy due to the emotional tone of sad music.

📊 Confidence: 42%
⚠️  Low confidence (< 0.5): top result scored below 50% of max. Recommendations may be weak matches.
```

**What to observe:**
- ⚠️ Confidence is LOW (0.42) — system recognized the mismatch!
- ⚠️ Guardrails warned the user
- ✅ This shows the system is honest about uncertainty

---

### 4.5 Try Your Own Requests

Try a few more:
```
> lofi hip hop beats
> upbeat happy music for a road trip
> ambient background music for focus
> sad songs for a rainy day
```

For each, note:
- Did the genre/mood match?
- Is the confidence score high (>0.7) or low (<0.5)?
- Does the explanation make sense?
- Were the step logs printed?

---

## Step 5: Exit Interactive Mode

Type:
```
> quit
```

Or press `Ctrl+C` to force exit.

---

## Troubleshooting

### "GOOGLE_API_KEY environment variable not set"

**Problem**: The `.env` file wasn't loaded or the key is missing.

**Solution**:
```bash
# Make sure .env exists
ls -la .env
# Should print: -rw-r--r-- ... .env

# Check the key is there
cat .env
# Should print: GOOGLE_API_KEY=AIzaSyD...

# If key is wrong, get a new one from:
# https://aistudio.google.com/app/apikey
```

---

### "ModuleNotFoundError: No module named 'google'"

**Problem**: google-generativeai not installed.

**Solution**:
```bash
# Install it
pip install -q google-generativeai

# Verify
python3 -c "import google.generativeai; print('OK')"
```

---

### "The model 'gemini-1.5-flash' does not support..."

**Problem**: API returned an error about the model.

**Solution**:
- Check your API key is correct
- Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) and verify you're using the right key
- Gemini 1.5 Flash should be available on all free tier accounts

---

### System hangs / doesn't respond

**Problem**: Waiting for Gemini API response (takes 2-5 seconds per query).

**Solution**:
- Wait 10 seconds before giving up
- If still stuck, press `Ctrl+C` to cancel
- Check your internet connection
- Verify API key is valid

---

## What's Actually Happening Behind the Scenes

For each user query, here's the flow:

```
1. USER TYPES: "something chill for studying"
   ↓
2. GUARDRAILS CHECK: ✓ input is non-empty, <500 chars, no injection
   ↓
3. AGENT STEP 1: Gemini API call → parse intent
   Response: {genre: "lofi", mood: "chill", energy: 0.35}
   ↓
4. AGENT STEP 2: Load genre_lofi.txt + mood_chill.txt from disk
   RAG context retrieved: "Lo-fi... slower tempos (70-90 BPM)..."
   ↓
5. AGENT STEP 3: Score all 18 songs using base recommender
   Library Rain: 9.0/10.5 (highest)
   Midnight Coding: 8.71/10.5
   ... etc ...
   ↓
6. AGENT STEP 4: Gemini API call → generate explanation
   Input: top 5 songs + RAG context
   Output: "These recommendations combine lo-fi and ambient..."
   ↓
7. AGENT STEP 5: Confidence = 9.0 / 10.5 = 0.86
   Check: 0.86 > 0.7 ✓ No warning needed
   ↓
8. USER SEES: Top 5 songs + explanation + confidence score
```

All costs are covered by Gemini's free tier (60 req/min, no credit card).

---

## Success Checklist

After testing, you should see:

- ✅ All 5 agent steps execute and log to console
- ✅ Top recommendations match the user's mood/genre preference
- ✅ Confidence scores are high (>0.7) for consistent preferences
- ✅ Confidence scores are low (<0.5) for conflicting preferences
- ✅ Explanations reference RAG knowledge (e.g., "acousticness", "tempos")
- ✅ System gracefully handles edge cases with warnings
- ✅ No credit card charges (free Gemini tier)

## Optional: Run the Evaluation Harness

If you want to test the system against predefined test cases:

```bash
pytest tests/test_evaluation.py -v
```

This runs 5 scenarios (chill study, high-energy workout, happy vibes, etc.) and reports PASS/FAIL for each.

---

## Optional: Record a Demo Video

For your portfolio, consider recording a short Loom video (2-3 min) showing:
- 2-3 different music requests
- All 5 agent steps executing in real-time
- The final recommendations + confidence scores

This is optional but great for demonstrating the system to others.

---

**Happy testing!** 🎵
