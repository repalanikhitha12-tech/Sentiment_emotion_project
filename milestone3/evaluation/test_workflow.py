
from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)


def evaluate_workflow():
    emotional_state = {
        "dominant_emotion": "fear",
        "intensity_level": "high",
    }

    preferences = ["relaxation"]
    history = {"liked": ["calm_music"]}

    results = get_ranked_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history=history,
        top_n=3,
    )

    print("\n=== Recommendation Workflow Evaluation ===")
    print("Emotion:", emotional_state["dominant_emotion"])
    print("Intensity:", emotional_state["intensity_level"])
    print("Preferences:", preferences)

    print("\nRanked recommendations:")

    for rank, item in enumerate(results, start=1):
        print(
            f"{rank}. {item['title']} | "
            f"Hybrid score: {item['hybrid_score']} | "
            f"Ranking score: {item['ranking_score']}"
        )

    assert len(results) <= 3

    scores = [item["ranking_score"] for item in results]
    assert scores == sorted(scores, reverse=True)

    ids = [item["id"] for item in results]
    assert len(ids) == len(set(ids))

    print("\nAll workflow checks passed!")


if __name__ == "__main__":
    evaluate_workflow()