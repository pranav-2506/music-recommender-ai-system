"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main              # Interactive mode
    python -m src.main --batch      # Run predefined profiles
"""

import sys
import os

# Ensure 'src/' is on the path so modules can be imported
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
from recommender import load_songs, recommend_songs
from agent import run_agent

# ---------------------------------------------------------------------------
# User profiles to evaluate
# ---------------------------------------------------------------------------

PROFILES = [
    {
        "label": "Profile 1 — High-Energy Pop",
        "prefs": {"genre": "pop",  "mood": "happy",   "energy": 0.80, "valence": 0.80},
    },
    {
        "label": "Profile 2 — Chill Lofi Study",
        "prefs": {"genre": "lofi", "mood": "chill",   "energy": 0.35, "valence": 0.60},
    },
    {
        "label": "Profile 3 — Intense Rock Workout",
        "prefs": {"genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.40},
    },
    {
        "label": "Profile 4 — Edge Case: High-Energy + Sad",
        "prefs": {"genre": "edm",  "mood": "sad",     "energy": 0.95, "valence": 0.25},
    },
]

# ---------------------------------------------------------------------------
# Experiment: double energy weight, halve genre weight
# ---------------------------------------------------------------------------
# Default:    energy=3.0, genre=1.5
# Experiment: energy=6.0, genre=0.75
# This tests whether the system becomes purely energy-driven when the
# energy signal is amplified — does mood/genre still matter at all?

EXPERIMENT_WEIGHTS = {
    "energy": 6.0,   # doubled
    "genre":  0.75,  # halved
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def print_profile(label: str, prefs: dict, songs: list, weights=None) -> None:
    """Print a labeled recommendations block for one user profile."""
    results = recommend_songs(prefs, songs, k=5, weights=weights)

    print()
    print("=" * 56)
    print(f"  {label}")
    print("=" * 56)
    prefs_str = "  ".join(f"{k}={v}" for k, v in prefs.items())
    print(f"  Prefs : {prefs_str}")
    print("-" * 56)

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
        print()

    print("=" * 56)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def interactive_mode(songs: list) -> None:
    """Run interactive mode with the AI agent."""
    load_dotenv()

    print()
    print("🎵 Music Recommender AI System")
    print("=" * 56)
    print("Describe the music you're in the mood for (type 'quit' to exit):\n")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() == "quit":
            print("Goodbye! 👋")
            break

        if not user_input:
            print("Please describe the music you want.\n")
            continue

        result = run_agent(user_input, songs)

        print()
        print("-" * 56)
        if result["recommendations"]:
            print("✨ Top Recommendations:\n")
            for rank, (song, score, _) in enumerate(result["recommendations"], start=1):
                print(f"  {rank}. {song['title']} — {song['artist']}")
                print(f"     Genre: {song['genre']} | Mood: {song['mood']} | Score: {score:.2f}\n")

            print(f"💭 Why: {result['explanation']}\n")
            print(f"📊 Confidence: {result['confidence']:.0%}")
            if result["warning"]:
                print(f"   {result['warning']}")
        else:
            print(f"❌ {result['explanation']}\n")

        print("-" * 56)
        print()


def batch_mode(songs: list) -> None:
    """Run batch mode with predefined profiles."""
    for profile in PROFILES:
        print_profile(profile["label"], profile["prefs"], songs)

    print()
    print("*" * 56)
    print("  EXPERIMENT — Double Energy Weight / Halve Genre Weight")
    print("  energy: 3.0 → 6.0   |   genre: 1.5 → 0.75")
    print("  (re-running Profile 1: High-Energy Pop)")
    print("*" * 56)
    print_profile(
        "Experiment Result",
        PROFILES[0]["prefs"],
        songs,
        weights=EXPERIMENT_WEIGHTS,
    )


def main() -> None:
    songs = load_songs("data/songs.csv")

    if "--batch" in sys.argv:
        batch_mode(songs)
    else:
        interactive_mode(songs)


if __name__ == "__main__":
    main()
