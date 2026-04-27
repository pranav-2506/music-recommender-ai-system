import os
from pathlib import Path

KNOWLEDGE_DIR = Path(__file__).parent.parent / "data" / "knowledge"


def retrieve_context(genre: str, mood: str) -> str:
    """Retrieve genre and mood context docs and combine into a single context string.

    Returns up to ~500 chars of combined context for use in Claude prompts.
    Files are named genre_{genre}.txt and mood_{mood}.txt.
    """
    context_parts = []

    # Try to load genre doc
    genre_file = KNOWLEDGE_DIR / f"genre_{genre.lower()}.txt"
    if genre_file.exists():
        with open(genre_file, "r", encoding="utf-8") as f:
            context_parts.append(f.read())

    # Try to load mood doc
    mood_file = KNOWLEDGE_DIR / f"mood_{mood.lower()}.txt"
    if mood_file.exists():
        with open(mood_file, "r", encoding="utf-8") as f:
            context_parts.append(f.read())

    # Combine and truncate to ~500 chars
    combined = "\n\n".join(context_parts)
    if len(combined) > 500:
        combined = combined[:500] + "..."

    return combined
