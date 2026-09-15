from flask import Flask, render_template, request

from ingestion import (
    validate_text,
    read_txt_file,
    read_csv_file
)

from preprocessing import preprocess_text
from sentiment.vader_sentiment import analyze_sentiment

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)

from milestone2.config import BERT_MODEL_DIR
from milestone2.emotion.predict_emotion import predict_emotions


app = Flask(__name__)

# Number of successfully analyzed samples
analyzed_samples = 0


# --------------------------------------------------
# LOAD BERT MODEL
# --------------------------------------------------

print("Loading BERT emotion model...")

emotion_tokenizer = AutoTokenizer.from_pretrained(
    str(BERT_MODEL_DIR)
)

emotion_model = AutoModelForSequenceClassification.from_pretrained(
    str(BERT_MODEL_DIR)
)

print("BERT emotion model loaded successfully.")


# --------------------------------------------------
# MAIN ROUTE
# --------------------------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    global analyzed_samples

    result = None
    error = None
    source = None
    sentiment_result = None
    emotion_result = None
    input_text = None

    if request.method == "POST":

        # Get direct text input
        text_input = request.form.get(
            "text_input",
            ""
        ).strip()

        # Get uploaded file
        uploaded_file = request.files.get("file")

        # ==================================================
        # OPTION 1: DIRECT TEXT
        # ==================================================

        if text_input:

            valid, message = validate_text(
                text_input
            )

            if valid:

                input_text = text_input

                # ------------------------------
                # PREPROCESSING
                # ------------------------------

                processed_text = preprocess_text(
                    text_input
                )

                result = processed_text

                source = "Direct Text Input"

                # ------------------------------
                # VADER SENTIMENT
                # ------------------------------

                sentiment_result = analyze_sentiment(
                    text_input
                )

                # ------------------------------
                # BERT EMOTION
                # ------------------------------

                emotion_result = predict_emotions(
                    emotion_model,
                    emotion_tokenizer,
                    text_input
                )

                if sentiment_result and emotion_result:
                    analyzed_samples += 1

            else:

                error = message

        # ==================================================
        # OPTION 2: FILE UPLOAD
        # ==================================================

        elif uploaded_file and uploaded_file.filename:

            filename = uploaded_file.filename.lower()

            # --------------------------------------------------
            # TXT FILE
            # --------------------------------------------------

            if filename.endswith(".txt"):

                text, message = read_txt_file(
                    uploaded_file
                )

                if text is not None:

                    input_text = text

                    # ------------------------------
                    # PREPROCESSING
                    # ------------------------------

                    processed_text = preprocess_text(
                        text
                    )

                    result = processed_text

                    source = "TXT File"

                    # ------------------------------
                    # VADER SENTIMENT
                    # ------------------------------

                    sentiment_result = analyze_sentiment(
                        text
                    )

                    # ------------------------------
                    # BERT EMOTION
                    # ------------------------------

                    emotion_result = predict_emotions(
                        emotion_model,
                        emotion_tokenizer,
                        text
                    )

                    if sentiment_result and emotion_result:
                        analyzed_samples += 1

                else:

                    error = message

            # --------------------------------------------------
            # CSV FILE
            # --------------------------------------------------

            elif filename.endswith(".csv"):

                text, message = read_csv_file(
                    uploaded_file
                )

                if text is not None:

                    input_text = text

                    # ------------------------------
                    # PREPROCESSING
                    # ------------------------------

                    processed_text = preprocess_text(
                        text
                    )

                    result = processed_text

                    source = "CSV File"

                    # ------------------------------
                    # VADER SENTIMENT
                    # ------------------------------

                    sentiment_result = analyze_sentiment(
                        text
                    )

                    # ------------------------------
                    # BERT EMOTION
                    # ------------------------------

                    emotion_result = predict_emotions(
                        emotion_model,
                        emotion_tokenizer,
                        text
                    )

                    if sentiment_result and emotion_result:
                        analyzed_samples += 1

                else:

                    error = message

            # --------------------------------------------------
            # INVALID FILE
            # --------------------------------------------------

            else:

                error = (
                    "Invalid file format. "
                    "Only .txt and .csv files are supported."
                )

        # ==================================================
        # NOTHING PROVIDED
        # ==================================================

        else:

            error = (
                "Input text is empty. "
                "Please enter text or upload a file."
            )

    return render_template(
        "index.html",
        result=result,
        error=error,
        source=source,
        input_text=input_text,
        sentiment_result=sentiment_result,
        emotion_result=emotion_result,
        analyzed_samples=analyzed_samples
    )


# --------------------------------------------------
# RUN FLASK APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )