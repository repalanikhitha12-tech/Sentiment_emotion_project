import pandas as pd
import torch

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import (
    ISEAR_DATA_DIR,
    BERT_MODEL_DIR
)


# Your shortened ISEAR-derived dataset contains 4 emotions.
ISEAR_EMOTIONS = [
    "anger",
    "fear",
    "joy",
    "sadness"
]


def find_isear_file():
    """Find the ISEAR CSV file."""

    csv_files = list(
        Path(ISEAR_DATA_DIR).glob("*.csv")
    )

    if not csv_files:
        return None

    return csv_files[0]


def predict_emotion(model, tokenizer, text):
    """
    Predict the primary emotion using only
    the four emotions available in the benchmark.
    """

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True
    )

    model.eval()

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.sigmoid(
        outputs.logits
    )[0]

    # Model labels are:
    # joy, sadness, anger, fear, surprise, disgust
    model_emotions = [
        "joy",
        "sadness",
        "anger",
        "fear",
        "surprise",
        "disgust"
    ]

    # Keep only emotions present in the benchmark.
    available_indices = [
        model_emotions.index(emotion)
        for emotion in ISEAR_EMOTIONS
    ]

    available_probabilities = probabilities[
        available_indices
    ]

    highest_position = torch.argmax(
        available_probabilities
    ).item()

    predicted_emotion = ISEAR_EMOTIONS[
        highest_position
    ]

    confidence = float(
        available_probabilities[
            highest_position
        ]
    )

    return predicted_emotion, confidence


def main():

    print("=" * 70)
    print("MILESTONE 2 - TASK 6")
    print("ISEAR-DERIVED BENCHMARK VALIDATION")
    print("=" * 70)

    isear_file = find_isear_file()

    if isear_file is None:

        print("\nISEAR dataset not found.")

        print(
            f"\nExpected location:"
        )

        print(
            f"{ISEAR_DATA_DIR}\\isear.csv"
        )

        return

    print(
        f"\nDataset: {isear_file}"
    )

    # Read dataset.
    df = pd.read_csv(
        isear_file
    )

    print(
        f"Total rows in dataset: {len(df)}"
    )

    # Check required columns.
    required_columns = [
        "sentiment",
        "content"
    ]

    for column in required_columns:

        if column not in df.columns:

            raise ValueError(
                f"Missing required column: {column}"
            )

    # Rename columns to standard names.
    df = df.rename(
        columns={
            "content": "text",
            "sentiment": "emotion"
        }
    )

    # Clean text.
    df["text"] = (
        df["text"]
        .astype(str)
        .str.strip()
    )

    # Clean emotion labels.
    df["emotion"] = (
        df["emotion"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # Keep only the four benchmark emotions.
    df = df[
        df["emotion"].isin(
            ISEAR_EMOTIONS
        )
    ]

    # Remove empty text.
    df = df[
        df["text"] != ""
    ]

    if len(df) == 0:

        raise ValueError(
            "No valid benchmark records found."
        )

    print(
        f"Valid benchmark examples: {len(df)}"
    )

    print(
        "\nEmotion distribution:"
    )

    print(
        df["emotion"].value_counts()
    )

    # Load trained BERT model.
    print(
        "\nLoading BERT model..."
    )

    tokenizer = AutoTokenizer.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(BERT_MODEL_DIR)
    )

    print(
        "BERT model loaded successfully."
    )

    predictions = []
    confidences = []

    print(
        "\nRunning benchmark predictions..."
    )

    for number, text in enumerate(
        df["text"],
        start=1
    ):

        prediction, confidence = predict_emotion(
            model,
            tokenizer,
            text
        )

        predictions.append(
            prediction
        )

        confidences.append(
            confidence
        )

        if number % 500 == 0:

            print(
                f"Processed {number} examples..."
            )

    true_labels = (
        df["emotion"]
        .tolist()
    )

    # Calculate metrics.
    accuracy = accuracy_score(
        true_labels,
        predictions
    )

    precision = precision_score(
        true_labels,
        predictions,
        labels=ISEAR_EMOTIONS,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        true_labels,
        predictions,
        labels=ISEAR_EMOTIONS,
        average="macro",
        zero_division=0
    )

    macro_f1 = f1_score(
        true_labels,
        predictions,
        labels=ISEAR_EMOTIONS,
        average="macro",
        zero_division=0
    )

    average_confidence = (
        sum(confidences)
        / len(confidences)
    )

    # Count incorrect predictions.
    incorrect_predictions = sum(
        true != predicted
        for true, predicted
        in zip(
            true_labels,
            predictions
        )
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "ISEAR BENCHMARK RESULTS"
    )

    print(
        "=" * 70
    )

    print(
        f"Accuracy            : {accuracy:.4f}"
    )

    print(
        f"Macro Precision     : {precision:.4f}"
    )

    print(
        f"Macro Recall        : {recall:.4f}"
    )

    print(
        f"Macro F1            : {macro_f1:.4f}"
    )

    print(
        f"Average Confidence  : {average_confidence:.4f}"
    )

    print(
        f"Incorrect Predictions: {incorrect_predictions}"
    )

    # Emotion-wise performance.
    print(
        "\n" + "=" * 70
    )

    print(
        "EMOTION-WISE PERFORMANCE"
    )

    print(
        "=" * 70
    )

    report = classification_report(
        true_labels,
        predictions,
        labels=ISEAR_EMOTIONS,
        target_names=ISEAR_EMOTIONS,
        zero_division=0
    )

    print(report)

    print(
        "=" * 70
    )

    print(
        "ISEAR BENCHMARK VALIDATION COMPLETED"
    )

    print(
        "=" * 70
    )


if __name__ == "__main__":
    main()