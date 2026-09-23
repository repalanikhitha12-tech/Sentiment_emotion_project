import pytest

from milestone3.feedback.feedback_learner import (
    record_feedback,
    calculate_feedback_score,
)


def test_record_liked_feedback():
    history = {}

    updated = record_feedback(
        history, "calm_music", "liked"
    )

    assert updated["feedback"] == [
        {
            "recommendation_id": "calm_music",
            "feedback": "liked",
        }
    ]


def test_liked_feedback_score():
    history = {
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            }
        ]
    }

    assert calculate_feedback_score(
        history, "calm_music"
    ) == 2


def test_disliked_feedback_score():
    history = {
        "feedback": [
            {
                "recommendation_id": "journal",
                "feedback": "disliked",
            }
        ]
    }

    assert calculate_feedback_score(
        history, "journal"
    ) == -2


def test_multiple_feedback_scores():
    history = {
        "feedback": [
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            },
            {
                "recommendation_id": "calm_music",
                "feedback": "liked",
            },
            {
                "recommendation_id": "calm_music",
                "feedback": "disliked",
            },
        ]
    }

    assert calculate_feedback_score(
        history, "calm_music"
    ) == 2


def test_invalid_feedback():
    with pytest.raises(ValueError):
        record_feedback({}, "journal", "maybe")


def test_original_history_not_modified():
    history = {"liked": ["calm_music"]}

    updated = record_feedback(
        history, "journal", "liked"
    )

    assert "feedback" not in history
    assert len(updated["feedback"]) == 1