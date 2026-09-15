from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import DISTILBERT_MODEL_DIR
from milestone2.emotion.predict_emotion import predict_emotions


print("Loading DistilBERT model...")

tokenizer = AutoTokenizer.from_pretrained(
    str(DISTILBERT_MODEL_DIR)
)

model = AutoModelForSequenceClassification.from_pretrained(
    str(DISTILBERT_MODEL_DIR)
)

text = "I am very happy and excited today!"

result = predict_emotions(
    model,
    tokenizer,
    text
)

print("\nPredicted emotions:", result["predicted_emotions"])
print("Primary emotion:", result["primary_emotion"])
print("Confidence:", f"{result['confidence']:.4f}")

print("\nEmotion probabilities:")

for emotion, probability in result["probabilities"].items():
    print(f"{emotion}: {probability:.4f}")