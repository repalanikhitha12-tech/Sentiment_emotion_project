
import json
from pathlib import Path
from datetime import datetime


FEEDBACK_FILE = Path("milestone4/data/feedback_history.json")


def load_feedback_history():
    """Load saved recommendation feedback."""
    if not FEEDBACK_FILE.exists():
        return []

    try:
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_feedback(recommendation_id, title, feedback):
    """Save feedback permanently to a JSON file."""
    if feedback not in ("liked", "disliked"):
        raise ValueError("Feedback must be 'liked' or 'disliked'.")

    records = load_feedback_history()

    records.append({
        "recommendation_id": recommendation_id,
        "title": title,
        "feedback": feedback,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    })

    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    return records