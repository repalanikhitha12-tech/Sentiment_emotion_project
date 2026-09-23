
import re
import nltk

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize


# Built-in English stopwords
stop_words = {
    "a", "an", "the", "and", "or", "but", "if", "while",
    "is", "am", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "at", "for", "with", "by",
    "from", "as", "it", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "me", "my",
    "your", "our", "their", "them", "his", "her", "its",
    "do", "does", "did", "have", "has", "had",
    "not", "no", "so", "too", "very"
}

lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    """
    Basic text preprocessing.
    """

    if text is None:
        return None

    text = text.strip()

    if text == "":
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Remove repeated spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenization
    tokens = wordpunct_tokenize(text)

    # Stop-word removal
    tokens = [
        word for word in tokens
        if word not in stop_words
    ]

    # Lemmatization
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
    ]

    return " ".join(tokens)