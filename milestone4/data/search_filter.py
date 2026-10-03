
from datetime import datetime


def filter_recommendation_history(
    history,
    start_date=None,
    end_date=None,
    emotion="All",
    intensity="All",
    recommendation_type="All",
    feedback_status="All",
):
    """Filter recommendation history using the selected criteria."""

    filtered = []

    for record in history:
        # Date filter
        timestamp = record.get("timestamp", "")

        try:
            record_date = datetime.fromisoformat(
                timestamp
            ).date()
        except (ValueError, TypeError):
            continue

        if start_date and record_date < start_date:
            continue

        if end_date and record_date > end_date:
            continue

        # Emotion filter
        emotional_state = record.get("emotional_state", {})
        if not isinstance(emotional_state, dict):
            emotional_state = {}

        dominant = emotional_state.get(
            "dominant_emotion", ""
        )

        if emotion != "All" and dominant != emotion.lower():
            continue

        # Intensity filter
        intensity_level = emotional_state.get(
            "intensity_level", ""
        )

        if (
            intensity != "All"
            and intensity_level.lower() != intensity.lower()
        ):
            continue

        # Recommendation type filter
        recommendations = record.get("recommendations", [])

        if recommendation_type != "All":
            titles = [
                item.get("title", "")
                for item in recommendations
                if isinstance(item, dict)
            ]

            if recommendation_type not in titles:
                continue

        # Feedback filter
        feedback = record.get("feedback", {})

        if not isinstance(feedback, dict):
            feedback = {}

        feedback_values = [
            str(value).lower()
            for value in feedback.values()
        ]

        if feedback_status == "Liked":
            if "liked" not in feedback_values:
                continue
        elif feedback_status == "Disliked":
            if "disliked" not in feedback_values:
                continue
        elif feedback_status == "No feedback":
            if feedback_values:
                continue

        filtered.append(record)

    return filtered