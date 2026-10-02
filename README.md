# MoodMentor – Sentiment and Emotion Analysis

## Project Overview

MoodMentor is a Python-based project designed to analyze text sentiment and emotions and provide personalized wellness recommendations. It aims to help users understand emotional patterns and explore activities that may support their well-being.

## Features

* Text input and file-based text ingestion
* Text preprocessing
* Baseline sentiment analysis using VADER
* Emotion classification for Joy, Sadness, Anger, Fear, Surprise, and Disgust
* Emotion intensity and emotional-state analysis
* Personalized wellness recommendations
* Hybrid recommendation engine
* Daily, weekly, and monthly emotion trend calculations
* Streamlit dashboard for emotion analysis and visualization
* Emotion history storage

## Technologies Used

* Python
* Flask
* Streamlit
* Pandas
* VADER Sentiment
* BERT and DistilBERT (for the emotion-classification work)
* Unit testing

## Project Structure

```text
Sentiment_emotion_project/
├── milestone1/
│   ├── ingestion.py
│   ├── preprocessing.py
│   └── sentiment/
├── milestone2/
│   └── emotion classification and dataset preparation
├── milestone3/
│   ├── emotion_analysis/
│   ├── recommendation/
│   ├── hybrid/
│   ├── ranking/
│   └── tests/
├── milestone4/
│   ├── dashboard/
│   │   └── app.py
│   ├── data/
│   │   ├── history.py
│   │   ├── trend.py
│   │   └── trend_chart.py
│   └── tests/
│       └── test_trend.py
├── app.py
└── requirements.txt
```

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/repalanikhitha12-tech/Sentiment_emotion_project.git
   cd Sentiment_emotion_project
   ```

2. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the Dashboard

If the project virtual environment already exists on Windows, run:

```powershell
.\.venv\Scripts\python.exe -m streamlit run milestone4\dashboard\app.py
```

Then open `http://localhost:8501` in your browser.

## Run Tests

Run Milestone 3 tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s milestone3\tests -p "test*.py" -v
```

Run Milestone 4 tests:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s milestone4\tests -p "test*.py" -v
```

## Current Test Results

* Milestone 3: 11 tests passed
* Milestone 4: 5 tests passed

## GitHub Repository

[Sentiment_emotion_project](https://github.com/repalanikhitha12-tech/Sentiment_emotion_project)

## Note

The dashboard's current emotion detection uses keyword-based matching. The displayed emotion results may differ from results produced by a trained transformer model. Wellness recommendations are general suggestions and are not a substitute for professional mental-health care.
