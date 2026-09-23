from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)


def test_feedback_changes_recommendation_score():
    emotional_state = {
        "dominant_emotion": "fear",
        "intensity_level": "medium",
    }

    liked_history = {
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            }
        ]
    }

    disliked_history = {
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "disliked",
            }
        ]
    }

    liked_results = get_ranked_recommendations(
        emotional_state=emotional_state,
        history=liked_history,
        top_n=10,
    )

    disliked_results = get_ranked_recommendations(
        emotional_state=emotional_state,
        history=disliked_history,
        top_n=10,
    )

    liked_item = next(
        item for item in liked_results
        if item["id"] == "calm_music"
    )

    disliked_item = next(
        item for item in disliked_results
        if item["id"] == "calm_music"
    )

    assert (
        liked_item["ranking_score"]
        > disliked_item["ranking_score"]
    )