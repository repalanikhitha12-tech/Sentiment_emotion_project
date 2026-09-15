import torch

from milestone2.config import PREDICTION_THRESHOLD
from milestone2.emotion.labels import EMOTION_LABELS


def predict_emotions(model, tokenizer, text):
    """
    Predict one or more emotions for the given text.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text input cannot be empty.")

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits into probabilities
    probabilities = torch.sigmoid(outputs.logits)[0]

    emotion_probabilities = {
        emotion: float(probabilities[index])
        for index, emotion in enumerate(EMOTION_LABELS)
    }

    # Select emotions above the prediction threshold
    predicted_emotions = [
        emotion
        for emotion, probability in emotion_probabilities.items()
        if probability >= PREDICTION_THRESHOLD
    ]

    # If nothing crosses the threshold, select the highest probability
    if not predicted_emotions:
        primary_emotion = max(
            emotion_probabilities,
            key=emotion_probabilities.get
        )
        predicted_emotions = [primary_emotion]

    primary_emotion = max(
        emotion_probabilities,
        key=emotion_probabilities.get
    )

    confidence = emotion_probabilities[primary_emotion]

    return {
        "text": text,
        "predicted_emotions": predicted_emotions,
        "primary_emotion": primary_emotion,
        "confidence": confidence,
        "probabilities": emotion_probabilities
    }