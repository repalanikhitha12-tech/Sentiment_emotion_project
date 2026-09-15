from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import BERT_MODEL_DIR
from milestone2.emotion.predict_emotion import predict_emotions


def load_bert_model():
    """Load the trained BERT model and tokenizer."""

    tokenizer = AutoTokenizer.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    return model, tokenizer


def predict_text(text):
    """Predict emotions for a text using the trained BERT model."""

    model, tokenizer = load_bert_model()

    return predict_emotions(
        model,
        tokenizer,
        text
    )


if __name__ == "__main__":

    text = input("Enter text: ").strip()

    if not text:
        print("Error: Text input cannot be empty.")
    else:
        result = predict_text(text)

        print("\nPredicted emotions:", result["predicted_emotions"])
        print("Primary emotion:", result["primary_emotion"])
        print(
            "Confidence:",
            f"{result['confidence']:.4f}"
        )

        print("\nEmotion probabilities:")

        for emotion, probability in result["probabilities"].items():
            print(
                f"{emotion}: {probability:.4f}"
            )