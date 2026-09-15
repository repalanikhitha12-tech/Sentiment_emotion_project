import pandas as pd
import torch

from torch.utils.data import Dataset

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments
)

from milestone2.config import (
    BERT_BASE_MODEL,
    BERT_MODEL_DIR,
    PROCESSED_DATA_DIR,
    MAX_LENGTH,
    EPOCHS,
    LEARNING_RATE,
    NUM_LABELS
)

from milestone2.emotion.labels import EMOTION_TO_ID


class EmotionDataset(Dataset):
    """Dataset for multi-label emotion classification."""

    def __init__(self, texts, labels, tokenizer):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):

        encoding = self.tokenizer(
            self.texts[index],
            truncation=True,
            padding="max_length",
            max_length=MAX_LENGTH,
            return_tensors="pt"
        )

        item = {
            key: value.squeeze(0)
            for key, value in encoding.items()
        }

        item["labels"] = torch.tensor(
            self.labels[index],
            dtype=torch.float
        )

        return item


def create_multi_label(emotion_text):
    """Convert emotion names into a multi-label vector."""

    label = [0.0] * NUM_LABELS

    emotions = [
        emotion.strip().lower()
        for emotion in str(emotion_text).split(",")
        if emotion.strip()
    ]

    for emotion in emotions:

        if emotion not in EMOTION_TO_ID:
            raise ValueError(
                f"Invalid emotion: {emotion}"
            )

        emotion_id = EMOTION_TO_ID[emotion]
        label[emotion_id] = 1.0

    return label


def train_bert():

    train_path = (
        PROCESSED_DATA_DIR /
        "train.csv"
    )

    if not train_path.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {train_path}"
        )

    df = pd.read_csv(train_path)

    df["text"] = (
        df["text"]
        .astype(str)
        .str.strip()
    )

    df["emotion"] = (
        df["emotion"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    tokenizer = AutoTokenizer.from_pretrained(
        BERT_BASE_MODEL
    )

    model = AutoModelForSequenceClassification.from_pretrained(
        BERT_BASE_MODEL,
        num_labels=NUM_LABELS,
        problem_type="multi_label_classification"
    )

    labels = [
        create_multi_label(emotion)
        for emotion in df["emotion"]
    ]

    emotion_dataset = EmotionDataset(
        df["text"].tolist(),
        labels,
        tokenizer
    )

    training_args = TrainingArguments(
        output_dir=str(BERT_MODEL_DIR),
        num_train_epochs=EPOCHS,
        learning_rate=LEARNING_RATE,
        per_device_train_batch_size=2,
        logging_steps=5,
        save_strategy="epoch",
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=emotion_dataset
    )

    print("=" * 60)
    print("Starting BERT training")
    print("=" * 60)

    print(f"Training examples: {len(df)}")
    print("Testing examples are NOT used during training.")

    trainer.train()

    trainer.save_model(
        str(BERT_MODEL_DIR)
    )

    tokenizer.save_pretrained(
        str(BERT_MODEL_DIR)
    )

    print("\nBERT training completed successfully.")
    print(
        f"Model saved to: {BERT_MODEL_DIR}"
    )


if __name__ == "__main__":
    train_bert()