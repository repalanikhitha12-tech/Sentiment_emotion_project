from transformers import AutoTokenizer
from milestone2.config import MAX_LENGTH


def load_tokenizer(model_name):
    """
    Load a Hugging Face tokenizer.
    """

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    return tokenizer


def tokenize_text(tokenizer, text):
    """
    Convert input text into tokens suitable for the Transformer model.
    """

    if not isinstance(text, str) or not text.strip():
        raise ValueError("Text input cannot be empty.")

    encoded = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )

    return encoded