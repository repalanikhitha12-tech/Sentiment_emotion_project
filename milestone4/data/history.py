import json
from datetime import datetime
from pathlib import Path


HISTORY_FILE = Path(__file__).resolve().parent / "emotion_history.json"


def _serialize_timestamp(timestamp):
    """
    Convert timestamp to a JSON-safe string.
    Supports both datetime objects and existing string timestamps.
    """
    if hasattr(timestamp, "isoformat"):
        return timestamp.isoformat()

    return str(timestamp)


def _deserialize_timestamp(timestamp):
    """
    Convert stored timestamp strings back to datetime objects.
    If conversion is not possible, keep the original value.
    """
    if isinstance(timestamp, datetime):
        return timestamp

    if isinstance(timestamp, str):
        try:
            return datetime.fromisoformat(timestamp)
        except ValueError:
            return timestamp

    return timestamp


def load_emotion_history():
    """
    Load emotion analysis history from the JSON file.
    """
    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        for item in data:
            if isinstance(item, dict) and "timestamp" in item:
                item["timestamp"] = _deserialize_timestamp(
                    item["timestamp"]
                )

        return data

    except (json.JSONDecodeError, OSError):
        return []


def save_emotion_record(emotion_scores, timestamp=None):
    """
    Save one emotion analysis record to history.

    Parameters:
        emotion_scores: Dictionary containing emotion probabilities/scores.
        timestamp: Optional datetime value.
    """
    if timestamp is None:
        timestamp = datetime.now()

    history = load_emotion_history()

    new_record = {
        "timestamp": timestamp,
        "emotion_scores": emotion_scores,
    }

    history.append(new_record)

    serialized_history = []

    for item in history:
        if not isinstance(item, dict):
            continue

        serialized_history.append(
            {
                "timestamp": _serialize_timestamp(
                    item.get("timestamp", datetime.now())
                ),
                "emotion_scores": item.get("emotion_scores", {}),
            }
        )

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            serialized_history,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return new_record