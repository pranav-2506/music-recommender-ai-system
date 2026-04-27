import json
import os
from typing import Any
from pathlib import Path

from dotenv import load_dotenv
import google.generativeai as genai
from guardrails import validate_input, validate_recommendations
from rag import retrieve_context
from recommender import recommend_songs

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Please check your .env file.")
genai.configure(api_key=api_key)
MODEL = "gemini-2.5-flash"


def parse_intent(user_input: str) -> dict[str, Any]:
    """Step 1: Use Gemini to parse user intent into structured preferences.

    Returns dict with keys: genre, mood, energy, valence (or defaults if parsing fails).
    """
    print("[Agent Step 1] Parsing user intent with Gemini...")

    prompt = f"""The user said: "{user_input}"

Extract their music preference as JSON with these fields (all optional, infer from context):
- genre: one of [pop, lofi, rock, edm, ambient, jazz, indie pop, synthwave, hip-hop, classical, folk, blues, metal, r&b, dream pop]
- mood: one of [happy, chill, intense, relaxed, focused, moody, sad, dreamy, energetic, euphoric, nostalgic, angry, melancholic, romantic]
- energy: float 0-1 (0.0 = very calm, 1.0 = very intense)
- valence: float 0-1 (0.0 = sad/dark, 1.0 = happy/bright)

Return ONLY valid JSON, no explanation. If you can't infer a field, omit it. Examples:
{{"genre": "lofi", "mood": "chill", "energy": 0.3}}
{{"mood": "intense", "energy": 0.9}}"""

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        parsed = json.loads(response.text)
        print(f"  Extracted prefs: {parsed}")
        return parsed
    except (json.JSONDecodeError, Exception):
        print(f"  ⚠️  Failed to parse intent. Using defaults.")
        return {"mood": "chill", "energy": 0.5}


def retrieve_knowledge(genre: str, mood: str) -> str:
    """Step 2: Retrieve genre and mood knowledge docs via RAG."""
    print(f"[Agent Step 2] Retrieving context for {genre}/{mood}...")
    context = retrieve_context(genre, mood)
    print(f"  Retrieved {len(context)} chars of context.")
    return context


def score_and_rank(prefs: dict, songs: list) -> list[tuple]:
    """Step 3: Score all songs using the recommender and return top 5."""
    print("[Agent Step 3] Scoring and ranking songs...")
    results = recommend_songs(prefs, songs, k=5)
    print(f"  Ranked {len(results)} unique songs.")
    return results


def generate_explanation(
    results: list[tuple], user_input: str, context: str
) -> str:
    """Step 4: Use Gemini to generate a natural language explanation.

    Uses RAG context to inform the explanation.
    """
    print("[Agent Step 4] Generating explanation with Gemini...")

    top_songs = "\n".join(
        [f"  {i+1}. {r[0]['title']} by {r[0]['artist']} (score: {r[1]:.2f})" for i, r in enumerate(results)]
    )

    prompt = f"""The user asked for music: "{user_input}"

Here's what we found:
{top_songs}

Here's relevant music knowledge:
{context}

Write a 2-3 sentence explanation of why these songs match their request. Be conversational and reference the mood/genre/vibe."""

    try:
        model = genai.GenerativeModel(MODEL)
        response = model.generate_content(prompt)
        explanation = response.text
        print(f"  Explanation generated.")
        return explanation
    except Exception as e:
        print(f"  ⚠️  Failed to generate explanation: {e}")
        return "Unable to generate explanation at this time."


def validate_output(results: list[tuple], prefs: dict) -> tuple[float, str]:
    """Step 5: Run guardrails on output and return confidence score."""
    print("[Agent Step 5] Validating recommendations...")
    confidence, warning = validate_recommendations(results, prefs)
    status = "✓" if confidence >= 0.7 else "⚠️"
    print(f"  Confidence: {confidence:.2f} {status}")
    if warning:
        print(f"  {warning}")
    return confidence, warning


def run_agent(user_input: str, songs: list) -> dict[str, Any]:
    """Run the full multi-step agentic workflow.

    Returns dict with:
      - recommendations: list of (song_dict, score, explanation)
      - explanation: natural language summary
      - confidence: confidence score 0-1
      - warning: any guardrail warning
    """
    # Validate input first
    is_valid, error = validate_input(user_input)
    if not is_valid:
        print(f"❌ Input validation failed: {error}")
        return {
            "recommendations": [],
            "explanation": error,
            "confidence": 0.0,
            "warning": error,
        }

    # Step 1: Parse intent
    prefs = parse_intent(user_input)

    # Ensure genre and mood have defaults for RAG
    genre = prefs.get("genre", "pop").lower()
    mood = prefs.get("mood", "happy").lower()

    # Step 2: Retrieve context
    context = retrieve_knowledge(genre, mood)

    # Step 3: Score and rank
    results = score_and_rank(prefs, songs)

    # Step 4: Generate explanation
    explanation = generate_explanation(results, user_input, context)

    # Step 5: Validate and score confidence
    confidence, warning = validate_output(results, prefs)

    return {
        "recommendations": results,
        "explanation": explanation,
        "confidence": confidence,
        "warning": warning,
    }
