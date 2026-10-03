
import json
import pytest

from milestone4.data import recommendation_history as history


def test_save_and_load_history(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history, "HISTORY_FILE", tmp_path / "history.json"
    )

    history.save_recommendation_history(
        user_text="I feel worried",
        emotional_state={"dominant_emotion": "fear"},
        emotion_probabilities={"fear": 0.4},
        recommendations=[{"id": "breathing", "title": "Breathing exercise"}],
    )

    loaded = history.load_recommendation_history()

    assert len(loaded) == 1
    assert loaded[0]["user_text"] == "I feel worried"
    assert loaded[0]["recommendations"][0]["id"] == "breathing"


def test_feedback_is_saved(tmp_path, monkeypatch):
    monkeypatch.setattr(
        history, "HISTORY_FILE", tmp_path / "history.json"
    )

    history.save_recommendation_history(
        user_text="I feel worried",
        emotional_state={"dominant_emotion": "fear"},
        emotion_probabilities={"fear": 0.4},
        recommendations=[{"id": "breathing"}],
    )

    timestamp = history.load_recommendation_history()[0]["timestamp"]

    updated = history.update_recommendation_feedback(
        timestamp, "breathing", "liked"
    )

    assert updated[0]["feedback"]["breathing"] == "liked"


def test_invalid_feedback_is_rejected():
    with pytest.raises(ValueError):
        history.update_recommendation_feedback(
            "some-timestamp", "breathing", "unknown"
        )


def test_history_survives_json_reload(tmp_path, monkeypatch):
    path = tmp_path / "history.json"
    monkeypatch.setattr(history, "HISTORY_FILE", path)

    history.save_recommendation_history(
        user_text="I feel happy",
        emotional_state={"dominant_emotion": "joy"},
        emotion_probabilities={"joy": 0.8},
        recommendations=[{"id": "music"}],
    )

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data[0]["emotional_state"]["dominant_emotion"] == "joy"