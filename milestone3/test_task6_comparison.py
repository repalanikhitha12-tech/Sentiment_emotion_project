
from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)

current_state = {
    "dominant_emotion": "joy",
    "intensity_level": "medium",
}

no_history = get_ranked_recommendations(
    emotional_state=current_state,
    preferences=[],
    history={},
    top_n=3,
)

fear_history = {
    "emotion_records": [
        {"emotion": "fear", "intensity": 0.8, "polarity": "negative"},
        {"emotion": "fear", "intensity": 0.7, "polarity": "negative"},
        {"emotion": "fear", "intensity": 0.6, "polarity": "negative"},
    ]
}

with_history = get_ranked_recommendations(
    emotional_state=current_state,
    preferences=[],
    history=fear_history,
    top_n=3,
)

print("\n--- WITHOUT EMOTION HISTORY ---")
for item in no_history:
    print(item["id"], item.get("ranking_score"))

print("\n--- WITH REPEATED FEAR HISTORY ---")
for item in with_history:
    print(item["id"], item.get("ranking_score"))

order_without = [item["id"] for item in no_history]
order_with = [item["id"] for item in with_history]

print("\nRecommendation order changed:", order_without != order_with)   