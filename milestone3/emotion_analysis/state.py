
"""
Task 1: Final Emotional State Analysis
"""

from milestone3.emotion_analysis.intensity import (
    normalize_probabilities,
    calculate_intensity,
    get_intensity_level,
    POSITIVE_EMOTIONS,
    NEGATIVE_EMOTIONS,
)


def analyze_emotional_state(
    probabilities,
    emotion_threshold=0.40,
):
    """
    Analyze dominant emotion, multiple emotions,
    confidence, polarity, mixed state and intensity.
    """

    probabilities = normalize_probabilities(
        probabilities
    )

    if not any(probabilities.values()):
        return {
            "dominant_emotion": "unknown",
            "multiple_emotions": [],
            "confidence": 0.0,
            "intensity": 0.0,
            "intensity_level": "low",
            "polarity": "neutral",
            "mixed_emotional_state": False,
            "emotional_state": "unknown",
        }

    dominant_emotion = max(
        probabilities,
        key=probabilities.get,
    )

    confidence = round(
        probabilities[dominant_emotion],
        4,
    )

    multiple_emotions = [
        emotion
        for emotion, probability
        in probabilities.items()
        if probability >= emotion_threshold
    ]

    positive_score = max(
        probabilities[e]
        for e in POSITIVE_EMOTIONS
    )

    negative_score = max(
        probabilities[e]
        for e in NEGATIVE_EMOTIONS
    )

    positive_detected = (
        positive_score >= emotion_threshold
    )

    negative_detected = (
        negative_score >= emotion_threshold
    )

    if positive_detected and negative_detected:
        polarity = "mixed"

    elif positive_detected:
        polarity = "positive"

    elif negative_detected:
        polarity = "negative"

    else:
        polarity = "neutral"

    mixed_emotional_state = (
        positive_detected and negative_detected
    )

    intensity = calculate_intensity(
        probabilities
    )

    intensity_level = get_intensity_level(
        intensity
    )

    if mixed_emotional_state:
        emotional_state = "mixed"

    else:
        emotional_state = dominant_emotion

    return {
        "dominant_emotion": dominant_emotion,
        "multiple_emotions": multiple_emotions,
        "confidence": confidence,
        "intensity": intensity,
        "intensity_level": intensity_level,
        "polarity": polarity,
        "mixed_emotional_state": (
            mixed_emotional_state
        ),
        "emotional_state": emotional_state,
        "emotion_probabilities": probabilities,
    }