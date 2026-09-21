
"""
Task 1: Dynamic Emotion Intensity Analysis
"""

EMOTION_LABELS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]

POSITIVE_EMOTIONS = {"joy", "surprise"}

NEGATIVE_EMOTIONS = {
    "sadness",
    "anger",
    "fear",
    "disgust",
}


def normalize_probabilities(probabilities):
    """
    Convert model probabilities into a valid dictionary.
    Supports small floating-point errors.
    """

    cleaned = {}

    for emotion in EMOTION_LABELS:
        value = float(probabilities.get(emotion, 0.0))
        cleaned[emotion] = max(0.0, min(1.0, value))

    return cleaned


def calculate_intensity(probabilities):
    """
    Calculate dynamic intensity from emotion probabilities.

    Output:
        0 to 100
    """

    probabilities = normalize_probabilities(probabilities)

    if not any(probabilities.values()):
        return 0.0

    # Strongest emotion probability
    maximum = max(probabilities.values())

    # Overall emotional activation
    average = sum(probabilities.values()) / len(
        EMOTION_LABELS
    )

    intensity = (
        0.70 * maximum +
        0.30 * average
    ) * 100

    return round(max(0.0, min(100.0, intensity)), 2)


def get_intensity_level(intensity):
    """
    Project-defined intensity bands.
    These are not clinical severity categories.
    """

    if intensity < 30:
        return "low"

    elif intensity < 60:
        return "moderate"

    else:
        return "high"