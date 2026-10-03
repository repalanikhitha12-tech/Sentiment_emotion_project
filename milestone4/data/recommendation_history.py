
import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("milestone4/data/recommendation_history.json")


def load_recommendation_history():
    """Load previously saved recommendation history."""
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_recommendation_history(
    user_text,
    emotional_state,
    emotion_probabilities,
    recommendations,
):
    """Save one analysis and its recommendations."""

    records = load_recommendation_history()

    record = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_text": user_text,
        "emotional_state": emotional_state,
        "emotion_probabilities": emotion_probabilities,
        "recommendations": recommendations,
        "feedback": {},
    }

    records.append(record)

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    return records


def update_recommendation_feedback(
    timestamp,
    recommendation_id,
    feedback,
):
    """Update feedback for a saved recommendation."""

    if feedback not in ("liked", "disliked"):
        raise ValueError("Feedback must be 'liked' or 'disliked'.")

    records = load_recommendation_history()

    for record in records:
        if record.get("timestamp") == timestamp:
            record.setdefault("feedback", {})[
                recommendation_id
            ] = feedback

            HISTORY_FILE.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with open(
                HISTORY_FILE,
                "w",
                encoding="utf-8",
            ) as file:
                json.dump(
                    records,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

            return records

    raise ValueError("Recommendation history record not found.")