from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import BERT_MODEL_DIR
from milestone2.emotion.predict_emotion import predict_emotions


def load_model():
    """Load the trained BERT model and tokenizer."""

    tokenizer = AutoTokenizer.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    return model, tokenizer


def run_test(model, tokenizer, test_name, text):
    """Run one edge-case test."""

    print("\n" + "=" * 70)
    print(f"TEST: {test_name}")
    print("=" * 70)

    print("Input:", repr(text))

    try:

        result = predict_emotions(
            model,
            tokenizer,
            text
        )

        print(
            "Predicted emotions:",
            result["predicted_emotions"]
        )

        print(
            "Primary emotion:",
            result["primary_emotion"]
        )

        print(
            "Confidence:",
            f"{result['confidence']:.4f}"
        )

        print("Probabilities:")

        for emotion, probability in result[
            "probabilities"
        ].items():

            print(
                f"  {emotion}: {probability:.4f}"
            )

        print("STATUS: PASS")

    except Exception as error:

        print("STATUS: ERROR")
        print("Message:", error)


def main():

    print("=" * 70)
    print("MILESTONE 2 - TASK 8")
    print("MODEL EDGE-CASE TESTING")
    print("=" * 70)

    model, tokenizer = load_model()

    test_cases = [

        (
            "Positive text",
            "I am very happy and excited today!"
        ),

        (
            "Negative text",
            "I am very sad and disappointed."
        ),

        (
            "Neutral text",
            "The meeting is scheduled for 10 AM."
        ),

        (
            "Mixed emotions",
            "I am happy about the result but worried about the future."
        ),

        (
            "Short text",
            "Happy!"
        ),

        (
            "Long text",
            "I had a wonderful day at college. "
            "I met my friends, completed my work, "
            "learned something new, and felt really "
            "happy about everything that happened today."
        ),

        (
            "Informal text",
            "OMG!!! This is sooo amazing 😂"
        ),

        (
            "Emoji text",
            "I got the result and I am so happy 😊🎉"
        ),

        (
            "Ambiguous text",
            "I don't know how I feel about this."
        ),

        (
            "Empty text",
            ""
        )
    ]

    for test_name, text in test_cases:

        run_test(
            model,
            tokenizer,
            test_name,
            text
        )

    print("\n" + "=" * 70)
    print("EDGE-CASE TESTING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()