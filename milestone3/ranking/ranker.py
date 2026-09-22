
def rank_recommendations(
    recommendations,
    emotion_match=0,
    intensity=0,
    preference_match=0,
    interaction_score=0
):
    """Rank recommendations by their combined scores."""

    ranked = []

    for item in recommendations:
        hybrid_score = item.get("hybrid_score", 0)

        score = (
            hybrid_score * 0.40
            + emotion_match * 0.20
            + intensity * 0.15
            + preference_match * 0.15
            + interaction_score * 0.10
        )

        result = item.copy()
        result["ranking_score"] = round(score, 2)
        ranked.append(result)

    ranked.sort(
        key=lambda item: item["ranking_score"],
        reverse=True
    )

    return ranked