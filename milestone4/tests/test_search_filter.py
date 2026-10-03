
from datetime import date

from milestone4.data.search_filter import (
    filter_recommendation_history,
)


def sample_history():
    return [
        {
            "timestamp": "2026-10-03T10:00:00",
            "emotional_state": {
                "dominant_emotion": "fear",
                "intensity_level": "medium",
            },
            "recommendations": [
                {"title": "Try a short breathing exercise"}
            ],
            "feedback": {"breathing_1": "liked"},
        },
        {
            "timestamp": "2026-10-02T10:00:00",
            "emotional_state": {
                "dominant_emotion": "joy",
                "intensity_level": "low",
            },
            "recommendations": [
                {"title": "Listen to calming music"}
            ],
            "feedback": {"music_1": "disliked"},
        },
    ]


def test_filter_by_emotion():
    result = filter_recommendation_history(
        sample_history(), emotion="fear"
    )
    assert len(result) == 1
    assert result[0]["emotional_state"]["dominant_emotion"] == "fear"


def test_filter_by_intensity():
    result = filter_recommendation_history(
        sample_history(), intensity="low"
    )
    assert len(result) == 1


def test_filter_by_recommendation_type():
    result = filter_recommendation_history(
        sample_history(),
        recommendation_type="Listen to calming music",
    )
    assert len(result) == 1


def test_filter_by_feedback():
    result = filter_recommendation_history(
        sample_history(), feedback_status="Liked"
    )
    assert len(result) == 1


def test_filter_by_date_range():
    result = filter_recommendation_history(
        sample_history(),
        start_date=date(2026, 10, 3),
        end_date=date(2026, 10, 3),
    )
    assert len(result) == 1