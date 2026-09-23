from milestone3.hybrid.engine import (
    generate_hybrid_recommendations,
)
from milestone3.ranking.ranker import (
    rank_recommendations,
)
from milestone3.recommendation.recommendation_data import (
    RECOMMENDATIONS,
)
from milestone3.feedback.feedback_learner import (
    calculate_feedback_score,
)

def get_ranked_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    preferences = preferences or []
    history = history or {}

    recommendations = generate_hybrid_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history=history,
        top_n=len(RECOMMENDATIONS),
    )
    # Task 7: Apply previous user feedback
    for item in recommendations:
        feedback_score = calculate_feedback_score(
            history,
            item["id"],
        )

        item["hybrid_score"] = (
            item.get("hybrid_score", 0)
            + feedback_score
        )
    intensity_level = emotional_state.get(
        "intensity_level", "medium"
    ).lower()

    intensity_scores = {
        "low": 3,
        "medium": 6,
        "high": 9,
    }

    intensity_score = intensity_scores.get(
        intensity_level, 6
    )

    emotion_match = (
        8
        if emotional_state.get("dominant_emotion")
        else 0
    )

    preference_match = 8 if preferences else 0
    interaction_score = 8 if history.get("liked") else 0

    ranked = rank_recommendations(
        recommendations,
        emotion_match=emotion_match,
        intensity=intensity_score,
        preference_match=preference_match,
        interaction_score=interaction_score,
    )

    return ranked[:top_n]