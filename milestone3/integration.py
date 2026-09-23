
"""
Milestone 3 - Complete Recommendation Integration

Connects:
1. Ranked recommendations
2. Feedback-aware scoring
3. Explainability
"""

from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)

from milestone3.explainability.explainer import (
    explain_recommendation,
)


def generate_final_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    """
    Generate ranked recommendations with explanations.
    """

    preferences = preferences or []
    history = history or {}

    recommendations = get_ranked_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history=history,
        top_n=top_n,
    )

    for item in recommendations:
        item["explanation"] = explain_recommendation(
            item=item,
            emotional_state=emotional_state,
            preferences=preferences,
            history=history,
        )

    return recommendations


if __name__ == "__main__":
    # Sample input for integration testing
    sample_emotional_state = {
        "dominant_emotion": "fear",
        "intensity_level": "high",
    }

    sample_preferences = ["relaxation"]

    sample_history = {
        "liked": ["calm_music"],
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            }
        ],
    }

    results = generate_final_recommendations(
        emotional_state=sample_emotional_state,
        preferences=sample_preferences,
        history=sample_history,
        top_n=3,
    )

    print("=== Milestone 3 Integrated Results ===")

    for rank, item in enumerate(results, start=1):
        print(f"\nRank: {rank}")
        print("ID:", item.get("id"))
        print("Title:", item.get("title"))
        print("Hybrid score:", item.get("hybrid_score"))
        print("Ranking score:", item.get("ranking_score"))
        print("Explanation:", item.get("explanation"))