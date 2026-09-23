
"""
Task 6: Emotional Trend & User State Tracking
"""

from collections import Counter, defaultdict


def add_emotion_record(history, record):
    """
    Add one emotion record without modifying
    the original history list.
    """
    if not isinstance(record, dict):
        raise ValueError("record must be a dictionary")

    updated_history = list(history)
    updated_history.append(dict(record))
    return updated_history


def analyze_emotion_history(history, recent_window=5):
    """
    Analyze historical emotion records.

    Each record may contain:
    {
        "emotion": "fear",
        "intensity": 0.8,
        "polarity": "negative",
        "timestamp": "2026-09-22T10:00:00"
    }
    """

    if recent_window < 1:
        raise ValueError("recent_window must be at least 1")

    if not history:
        return {
            "emotion_frequency": {},
            "average_intensity": 0.0,
            "dominant_emotion": "unknown",
            "polarity_trend": "unknown",
            "repeated_patterns": [],
            "recent_emotional_state": "unknown",
            "records_analyzed": 0,
        }

    records = [
        record for record in history
        if record.get("emotion")
    ]

    if not records:
        return {
            "emotion_frequency": {},
            "average_intensity": 0.0,
            "dominant_emotion": "unknown",
            "polarity_trend": "unknown",
            "repeated_patterns": [],
            "recent_emotional_state": "unknown",
            "records_analyzed": 0,
        }

    emotions = [
        str(record["emotion"]).lower()
        for record in records
    ]

    frequency = Counter(emotions)

    intensity_values = [
        float(record.get("intensity", 0.0))
        for record in records
    ]

    average_intensity = round(
        sum(intensity_values) / len(intensity_values),
        4,
    )

    dominant_emotion = frequency.most_common(1)[0][0]

    # Compare positive/negative polarity across time.
    midpoint = len(records) // 2

    if midpoint == 0:
        polarity_trend = "insufficient_data"
    else:
        earlier = records[:midpoint]
        later = records[midpoint:]

        def negative_ratio(group):
            negative = sum(
                1 for item in group
                if item.get("polarity") == "negative"
            )
            return negative / len(group)

        earlier_ratio = negative_ratio(earlier)
        later_ratio = negative_ratio(later)

        if later_ratio < earlier_ratio:
            polarity_trend = "more_positive"
        elif later_ratio > earlier_ratio:
            polarity_trend = "more_negative"
        else:
            polarity_trend = "stable"

    # Detect consecutive repeated emotions.
    repeated_patterns = []
    run_emotion = emotions[0]
    run_length = 1

    for emotion in emotions[1:]:
        if emotion == run_emotion:
            run_length += 1
        else:
            if run_length >= 2:
                repeated_patterns.append({
                    "emotion": run_emotion,
                    "consecutive_count": run_length,
                })
            run_emotion = emotion
            run_length = 1

    if run_length >= 2:
        repeated_patterns.append({
            "emotion": run_emotion,
            "consecutive_count": run_length,
        })

    recent_records = records[-recent_window:]
    recent_emotions = [
        str(record["emotion"]).lower()
        for record in recent_records
    ]

    recent_emotional_state = Counter(
        recent_emotions
    ).most_common(1)[0][0]

    return {
        "emotion_frequency": dict(frequency),
        "average_intensity": average_intensity,
        "dominant_emotion": dominant_emotion,
        "polarity_trend": polarity_trend,
        "repeated_patterns": repeated_patterns,
        "recent_emotional_state": recent_emotional_state,
        "records_analyzed": len(records),
    }