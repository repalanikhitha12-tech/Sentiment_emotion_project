EMOTION_LABELS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust"
]

# Convert emotion name to numerical label
EMOTION_TO_ID = {
    emotion: index
    for index, emotion in enumerate(EMOTION_LABELS)
}

# Convert numerical label back to emotion name
ID_TO_EMOTION = {
    index: emotion
    for index, emotion in enumerate(EMOTION_LABELS)
}


def get_emotion_id(emotion):
    """Return the numerical ID of an emotion."""
    emotion = emotion.lower().strip()

    if emotion not in EMOTION_TO_ID:
        raise ValueError(
            f"Invalid emotion: {emotion}. "
            f"Allowed emotions: {EMOTION_LABELS}"
        )

    return EMOTION_TO_ID[emotion]


def get_emotion_name(emotion_id):
    """Return the emotion name for a numerical ID."""

    if emotion_id not in ID_TO_EMOTION:
        raise ValueError(f"Invalid emotion ID: {emotion_id}")

    return ID_TO_EMOTION[emotion_id]