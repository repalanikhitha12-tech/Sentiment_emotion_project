
"""
Milestone 3 - Complete Integration

Connects BERT emotion probabilities to:
1. Emotional-state analysis
2. Ranked, feedback-aware recommendations
3. Recommendation explanations
"""

from milestone3.emotion_analysis.state import (
    analyze_emotional_state,
)
from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)
from milestone3.explainability.explainer import (
    explain_recommendation,
)


def generate_final_recommendations(
    emotion_probabilities,
    preferences=None,
    history=None,
    top_n=3,
):
    """Analyze emotion probabilities and recommend activities."""

    preferences = preferences or []
    history = history or {}

    emotional_state = analyze_emotional_state(
        emotion_probabilities
    )

    # Recommendation pipeline expects low/medium/high.
    # Map Task 1's "moderate" band to "medium".
    if emotional_state["intensity_level"] == "moderate":
        emotional_state["intensity_level"] = "medium"

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

    return {
        "emotional_state": emotional_state,
        "recommendations": recommendations,
    }


if __name__ == "__main__":
    # Sample probabilities for integration testing only.
    sample_probabilities = {
        "joy": 0.10,
        "sadness": 0.20,
        "anger": 0.15,
        "fear": 0.78,
        "surprise": 0.08,
        "disgust": 0.12,
    }

    results = generate_final_recommendations(
        emotion_probabilities=sample_probabilities,
        preferences=["relaxation"],
        history={
            "liked": ["calm_music"],
            "feedback": [
                {
                    "recommendation_id": "calm_music",
                    "feedback": "liked",
                }
            ],
        },
        top_n=3,
    )

    print("=== Emotional State ===")
    print(results["emotional_state"])

    print("\n=== Final Recommendations ===")
    for rank, item in enumerate(
        results["recommendations"],
        start=1,
    ):
        print(f"\nRank: {rank}")
        print("ID:", item.get("id"))
        print("Title:", item.get("title"))
        print("Ranking score:", item.get("ranking_score"))
        print("Explanation:", item.get("explanation"))