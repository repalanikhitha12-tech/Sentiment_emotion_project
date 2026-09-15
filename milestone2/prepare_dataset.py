import pandas as pd

from sklearn.model_selection import train_test_split

from milestone2.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    EMOTION_LABELS
)


def validate_emotions(emotion_text):
    """Validate and clean one or more emotion labels."""

    emotions = [
        emotion.strip().lower()
        for emotion in str(emotion_text).split(",")
        if emotion.strip()
    ]

    if not emotions:
        return None

    invalid_emotions = [
        emotion
        for emotion in emotions
        if emotion not in EMOTION_LABELS
    ]

    if invalid_emotions:
        return None

    emotions = list(dict.fromkeys(emotions))

    return ",".join(emotions)


def prepare_dataset(input_file):
    """
    Prepare the emotion dataset and create
    separate training and testing datasets.
    """

    input_path = RAW_DATA_DIR / input_file

    if not input_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {input_path}"
        )

    df = pd.read_csv(input_path)

    required_columns = ["text", "emotion"]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    # Clean text
    df["text"] = (
        df["text"]
        .astype(str)
        .str.strip()
    )

    # Remove empty text
    df = df[df["text"] != ""]

    # Validate emotions
    df["emotion"] = df["emotion"].apply(
        validate_emotions
    )

    # Remove invalid rows
    df = df.dropna(subset=["emotion"])

    # Remove duplicates
    df = df.drop_duplicates()

    if len(df) < 10:
        raise ValueError(
            "Dataset is too small for train/test splitting."
        )

    # Create train and test datasets
    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        shuffle=True
    )

    # Save complete processed dataset
    full_output = (
        PROCESSED_DATA_DIR /
        "emotion_dataset.csv"
    )

    df.to_csv(
        full_output,
        index=False
    )

    # Save training dataset
    train_output = (
        PROCESSED_DATA_DIR /
        "train.csv"
    )

    train_df.to_csv(
        train_output,
        index=False
    )

    # Save testing dataset
    test_output = (
        PROCESSED_DATA_DIR /
        "test.csv"
    )

    test_df.to_csv(
        test_output,
        index=False
    )

    print("Dataset prepared successfully.")
    print(f"Total rows : {len(df)}")
    print(f"Training rows: {len(train_df)}")
    print(f"Testing rows : {len(test_df)}")

    print(f"\nFull dataset : {full_output}")
    print(f"Training data: {train_output}")
    print(f"Testing data : {test_output}")

    print("\nTraining sample:")
    print(
        train_df.head(5).to_string(index=False)
    )

    print("\nTesting sample:")
    print(
        test_df.head(5).to_string(index=False)
    )


if __name__ == "__main__":
    prepare_dataset(
        "emotion_dataset_large.csv"
    )