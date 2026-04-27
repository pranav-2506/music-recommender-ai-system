# 🎵 Music Recommender AI System

**An intelligent music recommendation system with agentic AI, retrieval-augmented generation (RAG), and safety guardrails.**

This project extends the original content-based music recommender with Gemini-powered AI features: natural language intent parsing, knowledge-based explanations, and output validation. The system now understands conversational music requests and generates personalized recommendations with human-readable justifications.

---

## 🆕 AI Extensions (Project 4 Additions)

### 1. **Agentic Workflow** (`src/agent.py`)
A 5-step multi-turn orchestrator that uses Gemini to:
- **Step 1**: Parse natural language input → extract genre, mood, energy preferences
- **Step 2**: Retrieve relevant knowledge (genre/mood descriptions via RAG)
- **Step 3**: Score and rank songs using the base recommender
- **Step 4**: Generate AI-powered explanations of why songs match the request
- **Step 5**: Validate output confidence and surface guardrail warnings

Each step is logged to the console so reasoning is fully observable.

### 2. **Retrieval-Augmented Generation (RAG)** (`src/rag.py`)
Knowledge base with 8 text documents:
- **Genre docs**: `lofi.txt`, `pop.txt`, `rock.txt`, `edm.txt`, `ambient.txt`, `jazz.txt`
- **Mood docs**: `chill.txt`, `intense.txt`, `happy.txt`

RAG retrieves relevant documents and injects them into Gemini prompts, making explanations context-aware and reducing hallucination.

### 3. **Guardrails** (`src/guardrails.py`)
- **Input validation**: Checks for empty input, excessive length, and SQL injection patterns
- **Output confidence scoring**: Compares top result score (0-10.5) against max possible, returns confidence 0-1
- **Warning system**: Alerts users when recommendations are weak matches

### 4. **Evaluation Harness** (`tests/test_evaluation.py`)
Automated testing of the full AI pipeline on 5 predefined inputs:
```
✓ Chill Study Session    → expect lofi/ambient/jazz
✓ High-Energy Workout   → expect rock/edm/metal
✓ Happy Vibes           → expect pop/indie pop
✓ Moody Evening         → expect blues/classical
✓ Chill Electronic      → expect lofi/synthwave
```
Prints PASS/FAIL per case and overall score (e.g., 4/5 passed).

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   User Input (Natural Language)             │
│               e.g., "chill beats for studying"              │
└─────────────────┬───────────────────────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │   Agent (5 Steps)  │
        └─────────┬──────────┘
                  │
    ┌─────────────┼──────────────┬──────────────┬──────────────┐
    │             │              │              │              │
    ▼             ▼              ▼              ▼              ▼
[Parse Intent] [RAG Lookup] [Recommend] [Explain] [Validate]
    │             │              │              │              │
    │        ┌────▼────┐         │              │              │
    │        │Knowledge│         │              │              │
    │        │  Docs   │         │              │              │
    │        └─────────┘         │              │              │
    │                    ┌───────▼────────┐    │              │
    │                    │ Base Recommender│   │              │
    │                    │  (src/main.py)  │   │              │
    │                    └────────────────┘    │              │
    │                                           │              │
    └──────────────────────────────────────────┼──────────────┘
                                                │
                          ┌─────────────────────▼──────────┐
                          │ Final Output                    │
                          │ - Top 5 Songs                  │
                          │ - AI Explanation               │
                          │ - Confidence Score (0-1)       │
                          │ - Guardrail Warnings           │
                          └────────────────────────────────┘
```

---

## 📋 Features & Requirements Met

| Requirement | How It's Implemented |
|---|---|
| **Clear Project ID** | Extends `ai110-module3show-musicrecommendersimulation-starter` (Module 3 base system) |
| **Substantial AI Feature** | ✅ Agentic workflow (5-step reasoning chain) + RAG (knowledge base) + guardrails (validation) |
| **System Architecture Diagram** | ✅ ASCII flowchart above, PNG version in `/assets` |
| **End-to-End Demo** | ✅ Interactive CLI (`python -m src.main`) + batch mode (`python -m src.main --batch`) |
| **Reliability/Guardrails** | ✅ Input validation + output confidence scoring + evaluation harness with 5 test cases |
| **Documentation** | ✅ README (this file) + setup instructions + code comments |
| **Reflection** | ✅ Included at end of README |

---
## Watch the demo on loom
https://www.loom.com/share/79d42b7b3f9f478390cb7a1c38d9cd22

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Google Gemini API key (free tier, no credit card required)

### Installation

1. Clone the repo and navigate to it:
   ```bash
   cd music-recommender-ai-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate          # Mac/Linux
   # or .venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

### Running the System

**Interactive Mode** (with AI):
```bash
python3 -m src.main
```
Then type a music request like:
```
> something chill to study to, not too loud
[Agent Step 1] Parsing intent...
[Agent Step 2] Retrieving context...
[Agent Step 3] Scoring songs...
[Agent Step 4] Generating explanation...
[Agent Step 5] Confidence: 0.86 ✓
✨ Top Recommendations:
  1. Library Rain — Paper Lanterns
  2. Midnight Coding — LoRoom
  ...
```

**Batch Mode** (no API key needed, original profiles):
```bash
python3 -m src.main --batch
```
Runs 4 predefined profiles + experiment.

**Run Evaluation Harness**:
```bash
pytest tests/test_evaluation.py -v
```
Tests the agent on 5 diverse inputs and reports pass/fail.

**Run All Tests**:
```bash
pytest
```
Runs existing recommender tests + new evaluation harness.

---

## 📊 Sample Output

### Interactive Mode Example
```
> what kind of music helps you focus?

[Agent Step 1] Parsing user intent with Claude...
  Extracted prefs: {'genre': 'lofi', 'mood': 'focused', 'energy': 0.4}
[Agent Step 2] Retrieving context for lofi/focused...
  Retrieved 340 chars of context.
[Agent Step 3] Scoring and ranking songs...
  Ranked 5 unique songs.
[Agent Step 4] Generating explanation with Claude...
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

💭 Why: These recommendations combine lo-fi and ambient tracks that provide a calm, 
focused environment perfect for studying. The high acousticness and moderate tempos 
create an immersive atmosphere without distracting vocals or sudden intensity spikes.

📊 Confidence: 86%
```

---

## 🔍 How Each AI Component Works

### Intent Parser (Step 1)
Claude reads natural language and extracts structured preferences:
```python
# Input: "chill beats for late night studying"
# Output: {"genre": "lofi", "mood": "chill", "energy": 0.35}
```

### RAG (Step 2)
Loads relevant knowledge docs and injects them into the prompt:
```
Retrieved: "Lo-fi (Low Fidelity) Music... features jazzy chord progressions,
smooth samples, slower tempos (70-90 BPM)... perfect for studying, working..."
```
This context prevents hallucination and ensures AI explanations are factually grounded.

### Recommender (Step 3)
Uses the original content-based scoring system (no changes):
```
Library Rain: mood match (+2.5) + genre match (+1.5) + energy proximity (+3.0) = 9.0
```

### Explanation (Step 4)
Claude generates conversational summaries using the RAG context and scores:
```
"These recommendations combine lo-fi and ambient tracks that provide a calm, 
focused environment. High acousticness means organic, non-distracting instrumentation,
and the moderate tempos (70-80 BPM) match your preference for calm music."
```

### Guardrails (Step 5)
Validates:
- **Input**: non-empty, <500 chars, no SQL injection patterns
- **Output**: confidence = top_score / 10.5
  - ✓ High confidence (>0.7): top result scores >70% of max
  - ⚠️ Low confidence (<0.5): alert user to weak matches

---

## 🧪 Testing

### Unit Tests (Base Recommender)
```bash
pytest tests/test_recommender.py -v
```
Verifies original recommender functionality.

### Evaluation Tests (AI Pipeline)
```bash
pytest tests/test_evaluation.py -v
```
Tests intent parsing, RAG retrieval, scoring, and explanation generation on 5 real inputs.

### Manual Testing
```bash
python3 -m src.main
```
Interactive testing with your own queries.

---

## 📁 Project Structure

```
music-recommender-ai-system/
├── src/
│   ├── main.py                 # CLI entry point (interactive + batch modes)
│   ├── recommender.py          # Base content-based recommender (unchanged)
│   ├── agent.py                # 5-step AI workflow orchestrator
│   ├── rag.py                  # Knowledge base retrieval
│   └── guardrails.py           # Input/output validation
├── data/
│   ├── songs.csv               # 18-song catalog
│   └── knowledge/              # RAG knowledge base
│       ├── genre_lofi.txt
│       ├── genre_pop.txt
│       ├── genre_rock.txt
│       ├── genre_edm.txt
│       ├── genre_ambient.txt
│       ├── genre_jazz.txt
│       ├── mood_chill.txt
│       ├── mood_intense.txt
│       └── mood_happy.txt
├── tests/
│   ├── test_recommender.py     # Base recommender tests
│   └── test_evaluation.py      # AI pipeline evaluation harness
├── assets/
│   └── architecture.png        # System diagram (if exported from Mermaid)
├── requirements.txt            # Dependencies
├── .env.example                # API key template
├── README.md                   # This file
└── model_card.md               # Model transparency (from Module 3)
```

---

## 🎯 What This System Does Well

1. **Observable Reasoning**: Each agent step is logged, so you can see exactly how decisions are made.
2. **Grounded Explanations**: RAG ensures AI explanations are based on actual music knowledge, not hallucination.
3. **Safety-First**: Guardrails validate input and warn on low-confidence recommendations.
4. **Natural Interaction**: Users can request music in plain English, not structured forms.
5. **Transparent Scoring**: Every recommendation is traceable to a numeric score breakdown.

---

## ⚠️ Known Limitations

1. **Tiny Catalog**: Only 18 songs. Recommendations are limited to whatever subset matches the query.
2. **No Audio Analysis**: We use pre-computed features (energy, valence, etc.), not audio signals.
3. **No Listening History**: Each query is independent; the system doesn't learn from past preferences.
4. **Mood Overweighting**: The original recommender weights mood match at 2.5/10.5 (24%), which can dominate other signals.
5. **Genre Bias**: The dataset over-represents lofi/chill and under-represents metal/blues/classical.
6. **Claude Limitations**: Intent parsing relies on Claude's judgement; unusual phrasing might not parse correctly.

---

## 🤖 AI Collaboration & System Design Reflection

### How AI Was Used During Development

1. **Intent Parsing**: Claude API reads natural language and converts it to structured preferences (genre, mood, energy). This is the core of the agentic workflow.
2. **Explanation Generation**: Claude generates conversational summaries of why each song was recommended, using RAG-retrieved knowledge for context.
3. **Test Case Generation**: Used Claude to brainstorm 5 diverse test cases (chill, intense, happy, moody, electronic) that cover different recommendation scenarios.

### Helpful AI Suggestions

✅ **Multi-step reasoning chain** (the agentic workflow): Claude suggested breaking intent parsing, retrieval, scoring, explanation, and validation into explicit observable steps. This made the system far more debuggable and helped identify where failures occur.

✅ **RAG over fine-tuning**: Instead of fine-tuning Claude on music knowledge, Claude suggested loading genre/mood descriptions from disk. Much faster and more maintainable.

✅ **Confidence scoring**: Claude suggested measuring confidence as `top_score / max_possible_score`, a simple heuristic that turned out to be very useful for surfacing weak recommendations.

### Flawed AI Suggestions

❌ **Initial Design**: Claude first suggested adding a "critic step" where another Claude call would evaluate the top recommendation. This added cost and latency without improving quality. Removed it in favor of simpler guardrails.

❌ **Vector DB for RAG**: Claude initially suggested using FAISS or Pinecone for semantic retrieval. Unnecessary complexity for an 8-document knowledge base. Simple string matching works fine.

### Limitations & Future Work

- **No personalization**: The system doesn't remember past preferences. A real system would store user history and refine recommendations over time.
- **No collaborative filtering**: We only use content-based scoring. Spotify-style "users similar to you" would require millions of user-playlist pairs.
- **No audio embedding**: Modern recommenders use deep learning on audio spectrograms. Our system uses hand-crafted features.
- **Limited evaluation**: 5 test cases is a good start, but production systems need hundreds of diverse test cases and A/B testing with real users.
- **Cold-start problem**: New users get the same experience as everyone else. Real systems solve this with exploration or demographics.

---

## 📚 References

- **Base Recommender**: Original work from `ai110-module3show-musicrecommendersimulation-starter`
- **Agentic Reasoning**: Following the ReAct framework (Reason + Act), where an agent explicitly writes out its reasoning chain
- **RAG Pattern**: Inspired by Lewis et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
- **Guardrails**: Adapted from Ghai et al. "Guardrails: A Framework for Improving the Robustness of Conversational AI"

---

**Last updated**: April 2026  
**Author**: Pranav Chandar  
**License**: MIT
