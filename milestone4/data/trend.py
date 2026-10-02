from datetime import datetime, timedelta

EMOTIONS = [
    "joy", "sadness", "anger",
    "fear", "surprise", "disgust",
]


def add_emotion_record(records, emotion_scores, timestamp=None):
    """Add one emotional record to the history."""
    if timestamp is None:
        timestamp = datetime.now()

    records.append({
        "timestamp": timestamp,
        "emotion_scores": emotion_scores.copy(),
    })
    return records


def _get_timestamp(record):
    """Convert string timestamps to datetime objects."""
    timestamp = record["timestamp"]
    if isinstance(timestamp, str):
        timestamp = datetime.fromisoformat(timestamp)
    return timestamp


def _calculate_average(records, get_period):
    """Calculate average scores for each time period."""
    grouped_data = {}

    for record in records:
        timestamp = _get_timestamp(record)
        period = get_period(timestamp)

        if period not in grouped_data:
            grouped_data[period] = {
                emotion: [] for emotion in EMOTIONS
            }

        scores = record.get("emotion_scores", {})
        for emotion in EMOTIONS:
            score = scores.get(emotion, 0.0)
            grouped_data[period][emotion].append(float(score))

    averages = {}
    for period, emotions in grouped_data.items():
        averages[period] = {}
        for emotion, values in emotions.items():
            averages[period][emotion] = (
                sum(values) / len(values) if values else 0.0
            )

    return averages


def calculate_daily_average(records):
    """Calculate average emotion scores for each day."""
    return _calculate_average(
        records,
        lambda timestamp: timestamp.date(),
    )


def calculate_weekly_average(records):
    """Calculate average emotion scores for each week, starting Monday."""
    def get_week_start(timestamp):
        date = timestamp.date()
        return date - timedelta(days=date.weekday())

    return _calculate_average(records, get_week_start)


def calculate_monthly_average(records):
    """Calculate average emotion scores for each month."""
    return _calculate_average(
        records,
        lambda timestamp: timestamp.date().replace(day=1),
    )


def get_dominant_emotion(emotion_scores):
    """Return the emotion with the highest score."""
    if not emotion_scores:
        return None

    return max(emotion_scores, key=emotion_scores.get)
