
import json

import pytest

from milestone4.data import feedback_history


def test_save_and_load_feedback(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback_history.json"

    monkeypatch.setattr(
        feedback_history,
        "FEEDBACK_FILE",
        feedback_file,
    )

    feedback_history.save_feedback(
        "calm_music",
        "Calm Music",
        "liked",
    )

    records = feedback_history.load_feedback_history()

    assert len(records) == 1
    assert records[0]["recommendation_id"] == "calm_music"
    assert records[0]["title"] == "Calm Music"
    assert records[0]["feedback"] == "liked"
    assert "timestamp" in records[0]


def test_feedback_persists_in_json(tmp_path, monkeypatch):
    feedback_file = tmp_path / "feedback_history.json"

    monkeypatch.setattr(
        feedback_history,
        "FEEDBACK_FILE",
        feedback_file,
    )

    feedback_history.save_feedback(
        "calm_music",
        "Calm Music",
        "disliked",
    )

    with open(feedback_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data[0]["feedback"] == "disliked"


def test_invalid_feedback_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(
        feedback_history,
        "FEEDBACK_FILE",
        tmp_path / "feedback_history.json",
    )

    with pytest.raises(ValueError):
        feedback_history.save_feedback(
            "calm_music",
            "Calm Music",
            "neutral",
        )


def test_missing_feedback_file_returns_empty_list(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        feedback_history,
        "FEEDBACK_FILE",
        tmp_path / "missing.json",
    )

    assert feedback_history.load_feedback_history() == []