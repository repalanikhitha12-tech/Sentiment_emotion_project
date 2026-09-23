
from milestone3.history.emotion_tracker import (
    add_emotion_record,
    analyze_emotion_history,
)


def test_empty_history():
    result = analyze_emotion_history([])
    assert result["recent_emotional_state"] == "unknown"


def test_frequency_and_dominant_emotion():
    history = [
        {"emotion": "fear", "intensity": 0.8, "polarity": "negative"},
        {"emotion": "joy", "intensity": 0.4, "polarity": "positive"},
        {"emotion": "fear", "intensity": 0.7, "polarity": "negative"},
    ]

    result = analyze_emotion_history(history)

    assert result["emotion_frequency"]["fear"] == 2
    assert result["dominant_emotion"] == "fear"


def test_recent_state():
    history = [
        {"emotion": "fear", "intensity": 0.8, "polarity": "negative"},
        {"emotion": "joy", "intensity": 0.5, "polarity": "positive"},
        {"emotion": "joy", "intensity": 0.6, "polarity": "positive"},
    ]

    result = analyze_emotion_history(history, recent_window=2)
    assert result["recent_emotional_state"] == "joy"


def test_repeated_pattern():
    history = [
        {"emotion": "fear", "intensity": 0.8, "polarity": "negative"},
        {"emotion": "fear", "intensity": 0.7, "polarity": "negative"},
        {"emotion": "fear", "intensity": 0.6, "polarity": "negative"},
    ]

    result = analyze_emotion_history(history)

    assert result["repeated_patterns"] == [
        {"emotion": "fear", "consecutive_count": 3}
    ]


def test_add_record_does_not_change_original():
    original = []
    record = {"emotion": "joy", "intensity": 0.7}

    updated = add_emotion_record(original, record)

    assert original == []
    assert len(updated) == 1
    
from milestone3.hybrid.engine import (
    generate_hybrid_recommendations,
)


def test_historical_emotion_patterns_influence_scores():
    current_state = {
        "dominant_emotion": "joy",
        "intensity_level": "medium",
    }

    history_with_repeated_fear = {
        "emotion_records": [
            {"emotion": "fear", "intensity": 0.8, "polarity": "negative"},
            {"emotion": "fear", "intensity": 0.7, "polarity": "negative"},
            {"emotion": "fear", "intensity": 0.6, "polarity": "negative"},
        ]
    }

    results = generate_hybrid_recommendations(
        emotional_state=current_state,
        history=history_with_repeated_fear,
        top_n=10,
    )

    fear_items = [
        item for item in results
        if "fear" in [
            str(emotion).lower()
            for emotion in item.get("emotions", [])
        ]
    ]

    assert fear_items
    assert all(
        item["hybrid_score"] >= 2
        for item in fear_items
    )