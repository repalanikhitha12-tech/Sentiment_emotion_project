import json
from pathlib import Path
from datetime import datetime


HISTORY_FILE = Path(
    "milestone4/data/emotion_history.json"
)


def load_emotion_history():
    """
    Load stored emotion records from JSON.
    """

    if not HISTORY_FILE.exists():
        return []

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        for record in data:

            record["timestamp"] = datetime.fromisoformat(
                record["timestamp"]
            )

        return data

    except (json.JSONDecodeError, ValueError):

        return []


def save_emotion_record(
    emotion_scores,
    timestamp=None
):
    """
    Save one emotion record to JSON.
    """

    if timestamp is None:
        timestamp = datetime.now()

    records = load_emotion_history()

    record = {
        "timestamp": timestamp,
        "emotion_scores": emotion_scores.copy()
    }

    records.append(record)

    serializable_records = []

    for item in records:

        item_copy = {
            "timestamp": item["timestamp"].isoformat(),
            "emotion_scores": item["emotion_scores"]
        }

        serializable_records.append(item_copy)

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        HISTORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            serializable_records,
            file,
            indent=4
        )

    return records