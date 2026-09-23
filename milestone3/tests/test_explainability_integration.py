from milestone3.pipeline import generate_explained_recommendations


def test_pipeline_adds_explanations():
    emotional_state = {
        "dominant_emotion": "sadness",
        "intensity_level": "low",
    }

    recommendations = generate_explained_recommendations(
        emotional_state=emotional_state,
        preferences=["music"],
        history={},
        top_n=3,
    )

    assert len(recommendations) > 0

    for item in recommendations:
        assert "explanation" in item
        assert isinstance(item["explanation"], list)
        assert len(item["explanation"]) > 0