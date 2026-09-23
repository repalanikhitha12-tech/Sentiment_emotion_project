from milestone3.explainability.explainer import explain_recommendation


def test_explainer_mentions_matching_emotion():
    item = {
        "id": "calm_music",
        "emotions": ["sadness", "fear"],
        "intensity_levels": ["low"],
        "category": "music",
    }

    emotional_state = {
        "dominant_emotion": "sadness",
        "intensity_level": "low",
    }

    reasons = explain_recommendation(
        item,
        emotional_state,
        preferences=["music"],
        history={},
    )

    assert any("sadness" in reason for reason in reasons)
    assert any("low" in reason for reason in reasons)
    assert any("music" in reason for reason in reasons)


def test_explainer_mentions_feedback():
    item = {
        "id": "calm_music",
        "emotions": [],
        "intensity_levels": [],
        "category": "music",
    }

    emotional_state = {}

    history = {
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            }
        ]
    }

    reasons = explain_recommendation(
        item,
        emotional_state,
        preferences=[],
        history=history,
    )

    assert any("positive" in reason for reason in reasons)


def test_explainer_has_fallback_reason():
    item = {
        "id": "general_activity",
        "emotions": [],
        "intensity_levels": [],
        "category": "general",
    }

    reasons = explain_recommendation(
        item,
        {},
        preferences=[],
        history={},
    )

    assert len(reasons) > 0