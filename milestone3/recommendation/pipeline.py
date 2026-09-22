
from milestone3.hybrid.engine import (
    generate_hybrid_recommendations,
)
from milestone3.ranking.ranker import (
    rank_recommendations,
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
        top_n=top_n,
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