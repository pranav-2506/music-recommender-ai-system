import re


def validate_input(user_input: str) -> tuple[bool, str]:
    """Validate user input for safety and reasonableness.

    Returns (is_valid, error_message).
    Checks: non-empty, reasonable length, no obvious injection patterns.
    """
    if not user_input or not user_input.strip():
        return False, "Input cannot be empty."

    if len(user_input) > 500:
        return False, f"Input too long ({len(user_input)} chars). Keep it under 500."

    # Check for SQL injection patterns (basic check)
    if re.search(r"(?i)(DROP|DELETE|INSERT|SELECT|UPDATE|;|--|/\*)", user_input):
        return False, "Input contains suspicious patterns. Please describe your music preference normally."

    return True, ""


def validate_recommendations(
    results: list[tuple], user_prefs: dict
) -> tuple[float, str]:
    """Score confidence in recommendations and return warnings if low.

    Results format: list of (song_dict, score, explanation).
    Confidence = top_song_score / 10.5 (max possible score).

    Returns (confidence_score_0_to_1, warning_message).
    """
    if not results:
        return 0.0, "No recommendations found. Try adjusting your preferences."

    top_score = results[0][1]
    max_possible_score = 10.5

    confidence = min(top_score / max_possible_score, 1.0)

    warning = ""
    if confidence < 0.5:
        warning = "⚠️  Low confidence (< 0.5): top result scored below 50% of max. Recommendations may be weak matches."
    elif confidence < 0.7:
        warning = "⚠️  Moderate confidence (0.5-0.7): consider browsing more results."

    return confidence, warning
