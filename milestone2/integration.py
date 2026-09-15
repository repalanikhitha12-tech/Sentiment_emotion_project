from milestone2.emotion.predict_emotion import predict_emotions


def run_emotion_classification(model, tokenizer, text):
    """
    Run emotion classification using the trained Transformer model.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text input cannot be empty.")

    return predict_emotions(
        model,
        tokenizer,
        text
    )