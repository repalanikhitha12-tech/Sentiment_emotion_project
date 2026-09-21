from milestone3.recommendation.personalized import (
    generate_recommendations,
)


def generate_hybrid_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    """
    Combine emotion, intensity, preference,
    and interaction history signals.
    """

    preferences = preferences or []
    history = history or {}

    # Get personalized recommendations from Task 2
    recommendations = generate_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history=history,
        top_n=len(
            __import__(
                "milestone3.recommendation.recommendation_data",
                fromlist=["RECOMMENDATIONS"],
            ).RECOMMENDATIONS
        ),
    )

    # Add hybrid-specific rule adjustments
    for item in recommendations:
        score = 0

        emotion = emotional_state.get(
            "dominant_emotion", ""
        )
        intensity = emotional_state.get(
            "intensity_level", "medium"
        )

        # Rule 1: Match detected emotion
        if emotion in item["emotions"]:
            score += 3

        # Rule 2: Match intensity
        if intensity in item["intensity_levels"]:
            score += 2

        # Rule 3: Match user preferences
        if item["category"] in preferences:
            score += 3

        # Rule 4: Previously liked item
        if item["id"] in history.get("liked", []):
            score += 2

        item["hybrid_score"] = score

    # Sort highest hybrid score first
    recommendations.sort(
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )

    # Remove duplicate IDs and return top results
    final_results = []
    seen_ids = set()

    for item in recommendations:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            final_results.append(item)

        if len(final_results) >= top_n:
            break

    return final_results