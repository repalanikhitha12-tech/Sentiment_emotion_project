
from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)


def test_hybrid_ranking_pipeline():
    state = {
        "dominant_emotion": "fear",
        "intensity_level": "high",
    }

    history = {"liked": ["calm_music"]}

    result = get_ranked_recommendations(
        emotional_state=state,
        preferences=["relaxation"],
        history=history,
        top_n=3,
    )

    assert len(result) == 3
    assert result[0]["id"] == "calm_breathing"

    scores = [item["ranking_score"] for item in result]
    assert scores == sorted(scores, reverse=True)

    for item in result:
        assert "hybrid_score" in item
        assert "ranking_score" in item


def test_pipeline_returns_empty_for_zero_top_n():
    result = get_ranked_recommendations(
        emotional_state={"dominant_emotion": "fear"},
        top_n=0,
    )

    assert result == []