from milestone3.ranking.ranker import rank_recommendations


def test_recommendations_are_ranked():
    recommendations = [
        {"name": "journal", "hybrid_score": 5},
        {"name": "calm_music", "hybrid_score": 7},
        {"name": "calm_breathing", "hybrid_score": 8},
    ]

    result = rank_recommendations(
        recommendations,
        emotion_match=8,
        intensity=7,
        preference_match=9,
        interaction_score=6
    )

    assert len(result) == 3
    assert result[0]["name"] == "calm_breathing"
    assert result[0]["ranking_score"] >= result[1]["ranking_score"]
    assert result[1]["ranking_score"] >= result[2]["ranking_score"]


def test_empty_recommendations():
    result = rank_recommendations([])
    assert result == []