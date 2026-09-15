import pandas as pd
import torch

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import (
    PROCESSED_DATA_DIR,
    BERT_MODEL_DIR,
    DISTILBERT_MODEL_DIR,
    EMOTION_LABELS,
    PREDICTION_THRESHOLD
)


def create_true_labels(emotion_text):
    """Convert emotion names into a multi-label vector."""

    labels = [0] * len(EMOTION_LABELS)

    emotions = [
        emotion.strip().lower()
        for emotion in str(emotion_text).split(",")
        if emotion.strip()
    ]

    for emotion in emotions:
        if emotion in EMOTION_LABELS:
            index = EMOTION_LABELS.index(emotion)
            labels[index] = 1

    return labels


def predict_labels(model, tokenizer, texts):
    """Generate multi-label predictions."""

    model.eval()

    predictions = []

    for text in texts:

        inputs = tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding=True
        )

        with torch.no_grad():
            outputs = model(**inputs)

        probabilities = torch.sigmoid(
            outputs.logits
        )[0]

        predicted = (
            probabilities >= PREDICTION_THRESHOLD
        ).int().tolist()

        # Select highest probability if
        # no emotion reaches the threshold.
        if sum(predicted) == 0:

            highest_index = torch.argmax(
                probabilities
            ).item()

            predicted[highest_index] = 1

        predictions.append(predicted)

    return predictions


def calculate_metrics(true_labels, predicted_labels):
    """Calculate evaluation metrics."""

    accuracy = accuracy_score(
        true_labels,
        predicted_labels
    )

    precision = precision_score(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0
    )

    recall = recall_score(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0
    )

    macro_f1 = f1_score(
        true_labels,
        predicted_labels,
        average="macro",
        zero_division=0
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "macro_f1": macro_f1
    }


def evaluate_model(
    model_name,
    model_path,
    texts,
    true_labels
):
    """Evaluate one Transformer model."""

    print("\n" + "=" * 60)
    print(f"Evaluating {model_name}")
    print("=" * 60)

    tokenizer = AutoTokenizer.from_pretrained(
        str(model_path)
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        str(model_path)
    )

    predicted_labels = predict_labels(
        model,
        tokenizer,
        texts
    )

    metrics = calculate_metrics(
        true_labels,
        predicted_labels
    )

    print(
        f"Accuracy : {metrics['accuracy']:.4f}"
    )

    print(
        f"Precision: {metrics['precision']:.4f}"
    )

    print(
        f"Recall   : {metrics['recall']:.4f}"
    )

    print(
        f"Macro F1 : {metrics['macro_f1']:.4f}"
    )

    return metrics


def main():

    test_path = (
        PROCESSED_DATA_DIR /
        "test.csv"
    )

    if not test_path.exists():
        raise FileNotFoundError(
            f"Test dataset not found: {test_path}"
        )

    test_df = pd.read_csv(test_path)

    test_df["text"] = (
        test_df["text"]
        .astype(str)
        .str.strip()
    )

    test_df["emotion"] = (
        test_df["emotion"]
        .astype(str)
        .str.strip()
    )

    texts = test_df["text"].tolist()

    true_labels = [
        create_true_labels(emotion)
        for emotion in test_df["emotion"]
    ]

    print("=" * 60)
    print("HELD-OUT TEST SET EVALUATION")
    print("=" * 60)

    print(
        f"Test examples: {len(test_df)}"
    )

    print(
        "These examples were NOT used during training."
    )

    bert_metrics = evaluate_model(
        "BERT",
        BERT_MODEL_DIR,
        texts,
        true_labels
    )

    distilbert_metrics = evaluate_model(
        "DistilBERT",
        DISTILBERT_MODEL_DIR,
        texts,
        true_labels
    )

    print("\n" + "=" * 60)
    print("BERT vs DistilBERT")
    print("=" * 60)

    print(
        f"BERT       Macro F1: "
        f"{bert_metrics['macro_f1']:.4f}"
    )

    print(
        f"DistilBERT Macro F1: "
        f"{distilbert_metrics['macro_f1']:.4f}"
    )

    if (
        bert_metrics["macro_f1"]
        > distilbert_metrics["macro_f1"]
    ):

        print("\nBetter model: BERT")

    elif (
        distilbert_metrics["macro_f1"]
        > bert_metrics["macro_f1"]
    ):

        print("\nBetter model: DistilBERT")

    else:

        print(
            "\nBoth models have the same Macro F1."
        )


if __name__ == "__main__":
    main()