
import csv
import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)
from reportlab.lib.styles import getSampleStyleSheet


def prepare_report_rows(records):
    """Convert history records into rows suitable for CSV and PDF."""

    rows = []

    for record in records:
        state = record.get("emotional_state", {})
        scores = record.get("emotion_scores", {})
        recommendations = record.get("recommendations", [])
        feedback = record.get("feedback", {})

        if not isinstance(state, dict):
            state = {}
        if not isinstance(scores, dict):
            scores = {}
        if not isinstance(recommendations, list):
            recommendations = []
        if not isinstance(feedback, dict):
            feedback = {}

        recommendation_titles = [
            str(item.get("title", ""))
            for item in recommendations
            if isinstance(item, dict)
        ]

        rows.append({
            "timestamp": str(record.get("timestamp", "")),
            "input_text": str(record.get("input_text", "")),
            "dominant_emotion": str(
                state.get("dominant_emotion", record.get("dominant_emotion", ""))
            ),
            "intensity": str(
                state.get("intensity_level", record.get("intensity_level", ""))
            ),
            "emotion_scores": "; ".join(
                f"{key}: {value}" for key, value in scores.items()
            ),
            "recommendations": "; ".join(recommendation_titles),
            "feedback": "; ".join(
                f"{key}: {value}" for key, value in feedback.items()
            ),
        })

    return rows


def generate_csv_report(records):
    """Return a CSV report as text."""

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

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

    return output.getvalue()


def generate_pdf_report(records):
    """Return a PDF report as bytes."""

    rows = prepare_report_rows(records)
    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25,
    )

    styles = getSampleStyleSheet()
    story = [
        Paragraph("Emotion Analysis Report", styles["Title"]),
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles["Normal"],
        ),
        Paragraph(f"Total records: {len(rows)}", styles["Normal"]),
        Spacer(1, 12),
    ]

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
        table_data.append([
            row["timestamp"],
            row["input_text"],
            row["dominant_emotion"],
            row["intensity"],
            row["emotion_scores"],
            row["recommendations"],
            row["feedback"],
        ])

    table = Table(
        table_data,
        repeatRows=1,
        colWidths=[75, 125, 75, 55, 105, 125, 85],
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#24476B")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EDF2F7"),
        ]),
    ]))

    story.append(table)
    document.build(story)

    return buffer.getvalue()