from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import DISTILBERT_MODEL_DIR
from milestone2.emotion.predict_emotion import predict_emotions


def main():

    print("Loading DistilBERT model...")

    tokenizer = AutoTokenizer.from_pretrained(
        str(DISTILBERT_MODEL_DIR)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(DISTILBERT_MODEL_DIR)
    )

    test_texts = [
        "I am very happy and cheerful today.",
        "I feel very sad and lonely.",
        "I am extremely angry about this situation.",
        "I am scared and nervous about what might happen.",
        "Wow! I did not expect this amazing news!",
        "This terrible smell makes me feel disgusted.",
        "I am happy about the result but also nervous about what comes next."
    ]

    for number, text in enumerate(test_texts, start=1):

        result = predict_emotions(
            model,
            tokenizer,
            text
        )

        print("\n" + "=" * 60)
        print(f"Test {number}")
        print("=" * 60)

        print("Text:", result["text"])
        print("Predicted emotions:", result["predicted_emotions"])
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


if __name__ == "__main__":
    main()