
from milestone4.reports.export_reports import (
    generate_csv_report,
    generate_pdf_report,
)


def sample_records():
    return [
        {
            "timestamp": "2026-10-03T10:30:00",
            "input_text": "I feel happy today",
            "emotional_state": {
                "dominant_emotion": "joy",
                "intensity_level": "Medium",
            },
            "emotion_scores": {
                "joy": 0.8,
                "sadness": 0.1,
            },
            "recommendations": [
                {"title": "Listen to music"}
            ],
            "feedback": {"Listen to music": "liked"},
        }
    ]


def test_csv_report_contains_history():
    csv_text = generate_csv_report(sample_records())

    assert "timestamp" in csv_text
    assert "I feel happy today" in csv_text
    assert "joy" in csv_text
    assert "Listen to music" in csv_text


def test_pdf_report_has_valid_header():
    pdf_bytes = generate_pdf_report(sample_records())

    assert pdf_bytes.startswith(b"%PDF")
    assert len(pdf_bytes) > 0


def test_empty_records_export():
    csv_text = generate_csv_report([])
    pdf_bytes = generate_pdf_report([])

    assert "timestamp" in csv_text
    assert pdf_bytes.startswith(b"%PDF")