import csv
import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
)


def _get_recommendation_title(item):
    """Return a readable recommendation title."""
    if isinstance(item, dict):
        return (
            item.get("title")
            or item.get("name")
            or item.get("recommendation")
            or item.get("activity")
            or item.get("id")
            or "Unknown recommendation"
        )

    return str(item)


def _get_recommendation_text(recommendations):
    """Convert recommendation objects into readable text."""
    if not recommendations:
        return ""

    if isinstance(recommendations, dict):
        recommendations = recommendations.get(
            "recommendations",
            [],
        )

    if not isinstance(recommendations, list):
        return str(recommendations)

    titles = []

    for item in recommendations:
        titles.append(_get_recommendation_title(item))

    return "; ".join(titles)


def _get_feedback_text(feedback):
    """Convert feedback dictionary into readable text."""
    if not feedback:
        return ""

    if isinstance(feedback, dict):
        values = []

        for recommendation_id, status in feedback.items():
            values.append(
                f"{recommendation_id}: {status}"
            )

        return "; ".join(values)

    return str(feedback)


def prepare_report_rows(records):
    """
    Convert recommendation history records into
    rows suitable for CSV and PDF reports.
    """

    rows = []

    for record in records:
        timestamp = record.get(
            "timestamp",
            "",
        )

        # Actual history field name
        input_text = record.get(
            "user_text",
            record.get("input_text", ""),
        )

        # Actual history field name
        emotion_scores = record.get(
            "emotion_probabilities",
            record.get("emotion_scores", {}),
        )

        emotional_state = record.get(
            "emotional_state",
            {},
        )

        dominant_emotion = emotional_state.get(
            "dominant_emotion",
            record.get("dominant_emotion", ""),
        )

        intensity = emotional_state.get(
            "intensity",
            record.get("intensity", ""),
        )

        intensity_level = emotional_state.get(
            "intensity_level",
            "",
        )

        # If intensity is already a text level,
        # use it directly.
        if isinstance(intensity, str):
            intensity_value = intensity
        elif intensity_level:
            intensity_value = str(
                intensity_level
            )
        else:
            intensity_value = str(
                intensity
            )

        recommendations = record.get(
            "recommendations",
            [],
        )

        feedback = record.get(
            "feedback",
            {},
        )

        rows.append(
            {
                "timestamp": str(timestamp),
                "input_text": str(input_text),
                "dominant_emotion": str(
                    dominant_emotion
                ),
                "intensity": intensity_value,
                "emotion_scores": str(
                    emotion_scores
                ),
                "recommendations": (
                    _get_recommendation_text(
                        recommendations
                    )
                ),
                "feedback": _get_feedback_text(
                    feedback
                ),
            }
        )

    return rows


def generate_csv_report(records):
    """Generate a CSV report from history records."""

    rows = prepare_report_rows(records)

    output = io.StringIO()

    fieldnames = [
        "timestamp",
        "input_text",
        "dominant_emotion",
        "intensity",
        "emotion_scores",
        "recommendations",
        "feedback",
    ]

    writer = csv.DictWriter(
        output,
        fieldnames=fieldnames,
    )

    writer.writeheader()

    for row in rows:
        writer.writerow(row)

    return output.getvalue()


def generate_pdf_report(records):
    """Generate a PDF report from history records."""

    rows = prepare_report_rows(records)

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20,
    )

    headers = [
        "Timestamp",
        "Input Text",
        "Dominant Emotion",
        "Intensity",
        "Emotion Scores",
        "Recommendations",
        "Feedback",
    ]

    table_data = [headers]

    for row in rows:
        table_data.append(
            [
                row["timestamp"],
                row["input_text"],
                row["dominant_emotion"],
                row["intensity"],
                row["emotion_scores"],
                row["recommendations"],
                row["feedback"],
            ]
        )

    if len(table_data) == 1:
        table_data.append(
            [
                "",
                "No records available",
                "",
                "",
                "",
                "",
                "",
            ]
        )

    table = Table(
        table_data,
        repeatRows=1,
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    6,
                ),
            ]
        )
    )

    document.build([table])

    buffer.seek(0)

    return buffer.getvalue()