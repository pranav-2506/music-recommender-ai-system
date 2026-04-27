"""
Evaluation harness for the Music Recommender AI System.

Tests the full agent pipeline (intent parsing → RAG → scoring → explanation) on
predefined inputs and validates that recommendations match expected genres.

Run with: pytest tests/test_evaluation.py -v
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from recommender import load_songs
from agent import run_agent


EVAL_CASES = [
    {
        "name": "Chill Study Session",
        "input": "I need something chill and calm for studying tonight, no loud music",
        "expected_genres": ["lofi", "ambient", "jazz"],
    },
    {
        "name": "High-Energy Workout",
        "input": "pump me up with intense, energetic music for the gym",
        "expected_genres": ["rock", "edm", "metal", "hip-hop"],
    },
    {
        "name": "Happy Vibes",
        "input": "put on something upbeat and happy to brighten my day",
        "expected_genres": ["pop", "indie pop", "r&b"],
    },
    {
        "name": "Moody Evening",
        "input": "I want dark, introspective music for late night reflection",
        "expected_genres": ["blues", "classical", "indie pop", "dream pop"],
    },
    {
        "name": "Chill Electronic",
        "input": "smooth electronic beats, not too intense, good for relaxing",
        "expected_genres": ["lofi", "edm", "synthwave"],
    },
]


def run_evaluation(songs: list) -> dict:
    """Run all evaluation cases and return results."""
    results = {
        "passed": 0,
        "failed": 0,
        "cases": [],
    }

    print()
    print("=" * 70)
    print("  EVALUATION HARNESS — Music Recommender AI System")
    print("=" * 70)
    print()

    for case in EVAL_CASES:
        print(f"▶ {case['name']}")
        print(f"  Input: \"{case['input']}\"")

        agent_result = run_agent(case["input"], songs)

        if not agent_result["recommendations"]:
            print(f"  ❌ FAIL — No recommendations returned")
            results["failed"] += 1
            results["cases"].append({
                "name": case["name"],
                "passed": False,
                "reason": "No recommendations",
            })
            print()
            continue

        top_song = agent_result["recommendations"][0][0]
        top_genre = top_song["genre"].lower()
        is_match = top_genre in case["expected_genres"]

        if is_match:
            print(f"  ✓ PASS — Top song: {top_song['title']} ({top_genre})")
            results["passed"] += 1
            results["cases"].append({
                "name": case["name"],
                "passed": True,
                "top_song": top_song["title"],
                "top_genre": top_genre,
            })
        else:
            print(f"  ❌ FAIL — Top song: {top_song['title']} ({top_genre})")
            print(f"     Expected genres: {case['expected_genres']}")
            results["failed"] += 1
            results["cases"].append({
                "name": case["name"],
                "passed": False,
                "reason": f"Top genre '{top_genre}' not in {case['expected_genres']}",
            })

        print(f"  Confidence: {agent_result['confidence']:.0%}")
        print()

    # Summary
    total = results["passed"] + results["failed"]
    percentage = (results["passed"] / total * 100) if total > 0 else 0

    print("=" * 70)
    print(f"  RESULTS: {results['passed']}/{total} passed ({percentage:.0f}%)")
    print("=" * 70)
    print()

    return results


def test_evaluation_harness():
    """Test the evaluation harness on all cases."""
    songs = load_songs("data/songs.csv")
    results = run_evaluation(songs)

    # For pytest: at least 3/5 cases should pass
    assert results["passed"] >= 3, f"Only {results['passed']}/5 cases passed. Expected >= 3."


if __name__ == "__main__":
    songs = load_songs("data/songs.csv")
    run_evaluation(songs)
