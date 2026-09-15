from pathlib import Path

# ==============================
# Project Paths
# ==============================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
ISEAR_DATA_DIR = DATA_DIR / "isear"

MODELS_DIR = BASE_DIR / "models"
BERT_MODEL_DIR = MODELS_DIR / "bert"
DISTILBERT_MODEL_DIR = MODELS_DIR / "distilbert"

REPORTS_DIR = BASE_DIR / "reports"

# ==============================
# Emotion Labels
# ==============================

EMOTION_LABELS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust"
]

NUM_LABELS = len(EMOTION_LABELS)

# ==============================
# Transformer Models
# ==============================

BERT_BASE_MODEL = "bert-base-uncased"

DISTILBERT_BASE_MODEL = "distilbert-base-uncased"

# ==============================
# Training Settings
# ==============================

MAX_LENGTH = 128

BATCH_SIZE = 8

EPOCHS = 2

LEARNING_RATE = 2e-5

# ==============================
# Prediction Settings
# ==============================

PREDICTION_THRESHOLD = 0.50

# ==============================
# Create Required Directories
# ==============================

DATA_DIR.mkdir(exist_ok=True)
RAW_DATA_DIR.mkdir(exist_ok=True)
PROCESSED_DATA_DIR.mkdir(exist_ok=True)
ISEAR_DATA_DIR.mkdir(exist_ok=True)

MODELS_DIR.mkdir(exist_ok=True)
BERT_MODEL_DIR.mkdir(exist_ok=True)
DISTILBERT_MODEL_DIR.mkdir(exist_ok=True)

REPORTS_DIR.mkdir(exist_ok=True)