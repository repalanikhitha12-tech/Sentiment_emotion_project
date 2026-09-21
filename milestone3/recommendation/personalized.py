from milestone3.recommendation.recommendation_data import (
    RECOMMENDATIONS,
)


def generate_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    """
    Generate recommendations based on emotion,
    intensity, preferences, and liked history.
    """

    preferences = preferences or []
    history = history or {}

    dominant_emotion = emotional_state.get(
        "dominant_emotion", ""
    )

    intensity_level = emotional_state.get(
        "intensity_level", "medium"
    )

    liked_items = history.get("liked", [])

    results = []

    for item in RECOMMENDATIONS:
        score = 0

        # Emotion matching
        if dominant_emotion in item["emotions"]:
            score += 3

        # Intensity matching
        if intensity_level in item["intensity_levels"]:
            score += 2

        # Preference matching
        if item["category"] in preferences:
            score += 3

        # Previously liked item
        if item["id"] in liked_items:
            score += 2

        if score > 0:
            results.append({
                **item,
                "score": score,
            })

    # Sort by score, highest first
    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    # Return only top_n recommendations
    return [
        {
            key: value
            for key, value in item.items()
            if key != "score"
        }
        for item in results[:top_n]
    ]