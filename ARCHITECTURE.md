# System Architecture Diagram

## Visual Flowchart

```
┌──────────────────────────────────────────────────────────────────┐
│                    USER INPUT                                    │
│          (Natural Language Music Request)                         │
│       e.g., "chill beats for studying"                           │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
           ┌──────────────────────────────┐
           │   GUARDRAILS: INPUT CHECK    │
           │  - Non-empty?                │
           │  - Length < 500 chars?       │
           │  - No injection patterns?    │
           └────────────┬─────────────────┘
                        │
                        ▼
        ┌────────────────────────────────────┐
        │    AGENTIC WORKFLOW (5 STEPS)      │
        └────────────┬───────────────────────┘
                     │
        ┌────────────┴────────────┬──────────────────┬──────────────┐
        │                         │                  │              │
        ▼                         ▼                  ▼              ▼
  ┌──────────────┐      ┌────────────────┐  ┌──────────────┐  ┌──────────┐
  │ STEP 1:      │      │ STEP 2: RAG    │  │ STEP 3:      │  │ STEP 4:  │
  │ Parse Intent │      │ Retrieval      │  │ Score &      │  │ Generate │
  │              │      │                │  │ Rank Songs   │  │ Explain  │
  │ Claude calls │      │ Load:          │  │              │  │          │
  │ → extract    │      │ - genre_*.txt  │  │ Uses original│  │ Claude   │
  │   genre,     │      │ - mood_*.txt   │  │ recommender  │  │ reads:   │
  │   mood,      │      │                │  │ (unchanged)  │  │ - Scores │
  │   energy     │      │ Returns ~300   │  │              │  │ - RAG    │
  │              │      │ chars context  │  │ Returns top 5│  │   context│
  │ Returns:     │      │                │  │ (song, score)│  │          │
  │ {genre,mood, │      │ Returns: str   │  │              │  │ Writes   │
  │  energy...}  │      │                │  │ Returns:     │  │ explanation
  └──────────────┘      └────────────────┘  └──────────────┘  │          │
                                                                 └──────────┘
                                                                      │
                                                                      ▼
                                                            ┌──────────────────┐
                                                            │ STEP 5: VALIDATE │
                                                            │                  │
                                                            │ Guardrails:      │
                                                            │ - Confidence =   │
                                                            │   top_score /    │
                                                            │   10.5           │
                                                            │ - Warn if < 0.7  │
                                                            │ - Check output   │
                                                            │   safety         │
                                                            │                  │
                                                            │ Returns:         │
                                                            │ - confidence     │
                                                            │ - warning        │
                                                            └──────────┬───────┘
                                                                       │
                                                                       ▼
                            ┌──────────────────────────────────────────────────┐
                            │           FINAL OUTPUT                           │
                            │                                                  │
                            │ ✨ Top 5 Recommendations:                       │
                            │   1. Song Title — Artist (genre, mood, score)   │
                            │   2. ...                                        │
                            │                                                  │
                            │ 💭 Why: [AI-generated explanation]              │
                            │                                                  │
                            │ 📊 Confidence: 0.86 (86%)                       │
                            │    [⚠️  warning if < 0.7]                       │
                            └──────────────────────────────────────────────────┘
```

## Data Flow Annotations

### Input → Processing → Output

**Input**: User's natural language request
- Example: "I want chill, focused music for late-night studying"

**Processing Path**:
1. **Step 1 (Intent)**: Claude API parses request → `{genre: "lofi", mood: "focused", energy: 0.4}`
2. **Step 2 (RAG)**: Load `genre_lofi.txt` + `mood_focused.txt` → "Lo-fi features jazzy progressions, slower tempos..."
3. **Step 3 (Score)**: Base recommender scores all 18 songs against `{genre, mood, energy}` → ranked list
4. **Step 4 (Explain)**: Claude reads top 5 songs + RAG context → generates conversational explanation
5. **Step 5 (Validate)**: Check confidence = 9.0 / 10.5 = 0.86 ✓ (high confidence, no warning)

**Output**: Recommendations + explanation + confidence score

---

## Component Interactions

### Who Checks What?

```
┌─────────────────────────────────────────────────────────────┐
│ GUARDRAILS LAYER (Tests & Validation)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ INPUT VALIDATION (guardrails.py)                            │
│ ├─ Non-empty check                                          │
│ ├─ Length limit (< 500 chars)                               │
│ └─ Injection pattern detection (SQL, etc.)                  │
│                                                              │
│ AGENT EXECUTION (agent.py)                                  │
│ ├─ Step 1: Intent parser (Claude)                           │
│ ├─ Step 2: RAG retriever (file lookup)                      │
│ ├─ Step 3: Recommender (base system)                        │
│ ├─ Step 4: Explainer (Claude + RAG context)                 │
│ └─ Step 5: Confidence scorer (guardrails.py)                │
│                                                              │
│ EVALUATION HARNESS (tests/test_evaluation.py)               │
│ ├─ 5 predefined inputs (study, workout, happy, etc.)        │
│ ├─ Run full pipeline on each                                │
│ └─ Check if top genre matches expected → PASS/FAIL          │
│                                                              │
│ HUMAN REVIEW (Developer / Teacher)                          │
│ ├─ Read explanations for clarity                            │
│ ├─ Spot-check confidence scores                             │
│ ├─ Verify edge cases handled gracefully                     │
│ └─ Assess whether recommendations match intent              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Design Decisions

1. **5-Step Observable Reasoning Chain**: Each step logs to console so users and developers can see exactly what happened. Transparency builds trust.

2. **File-Based RAG, Not Vector DB**: 8 text documents don't need semantic search. Simple keyword matching works and avoids external dependencies.

3. **Confidence = Score Ratio**: `top_score / 10.5` is a simple heuristic that immediately surfaced when recommendations were weak (e.g., high-energy + sad mood produces confidence ~0.42).

4. **Guardrails at Both Ends**: Input validation prevents malicious input; output confidence helps users understand result quality.

5. **Reuse Original Recommender Unchanged**: The base content-based system works well. The AI layer wraps and explains it, not replaces it.

---

## Testing the System

```
┌──────────────────────────────────────────┐
│   TEST MODES                             │
├──────────────────────────────────────────┤
│                                          │
│ 🔵 BATCH MODE (No API Key Needed)        │
│    python3 -m src.main --batch           │
│    → Runs 4 hardcoded profiles           │
│    → Tests base recommender + UI         │
│                                          │
│ 🟢 INTERACTIVE MODE (API Key Required)   │
│    python3 -m src.main                   │
│    > describe your music preference      │
│    [Full 5-step agent pipeline runs]     │
│    → Can test intent parsing, RAG, etc.  │
│                                          │
│ 🟡 EVALUATION HARNESS (API Key Required) │
│    pytest tests/test_evaluation.py -v    │
│    → Runs 5 predefined test cases        │
│    → Reports PASS/FAIL per case          │
│    → Measures success rate               │
│                                          │
└──────────────────────────────────────────┘
```
