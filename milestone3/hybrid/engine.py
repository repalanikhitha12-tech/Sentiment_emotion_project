
from milestone3.recommendation.personalized import (
    generate_recommendations,
)
from milestone3.history.emotion_tracker import (
    analyze_emotion_history,
)


def generate_hybrid_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    """
    Combine current emotion, intensity, preferences,
    interaction history, and historical emotion trends.
    """

    preferences = preferences or []
    history = history or {}

    # Analyze historical emotion records (Task 6)
    emotion_records = history.get("emotion_records", [])
    trend_summary = analyze_emotion_history(
        emotion_records
    )

    historical_dominant = trend_summary[
        "dominant_emotion"
    ]

    repeated_emotions = {
        pattern["emotion"]
        for pattern in trend_summary["repeated_patterns"]
    }

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

    for item in recommendations:
        score = 0

        current_emotion = emotional_state.get(
            "dominant_emotion", ""
        )
        intensity = emotional_state.get(
            "intensity_level", "medium"
        )

        item_emotions = {
            str(emotion).lower()
            for emotion in item.get("emotions", [])
        }

        # Rule 1: Match current emotion
        if current_emotion in item_emotions:
            score += 3

        # Rule 2: Match current intensity
        if intensity in item.get("intensity_levels", []):
            score += 2

        # Rule 3: Match user preferences
        if item.get("category") in preferences:
            score += 3

        # Rule 4: Previously liked item
        if item.get("id") in history.get("liked", []):
            score += 2

        # Task 6 Rule 5: Match historically dominant emotion
        if (
            historical_dominant != "unknown"
            and historical_dominant in item_emotions
        ):
            score += 1

        # Task 6 Rule 6: Match a repeated emotional pattern
        if item_emotions.intersection(repeated_emotions):
            score += 2

        item["hybrid_score"] = score

    recommendations.sort(
        key=lambda item: item["hybrid_score"],
        reverse=True,
    )

    final_results = []
    seen_ids = set()

    for item in recommendations:
        if item["id"] not in seen_ids:
            seen_ids.add(item["id"])
            final_results.append(item)

        if len(final_results) >= top_n:
            break

    return final_results