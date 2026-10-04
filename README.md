# MoodMentor – Sentiment and Emotion Analysis

## Project Overview

MoodMentor is a Python-based sentiment and emotion analysis project that analyzes user text, identifies emotions, evaluates emotional intensity, generates personalized wellness recommendations, tracks emotional trends, stores recommendation feedback, and provides an interactive Streamlit dashboard.

## Project Objectives

- Analyze sentiment from user text
- Identify major emotional states
- Analyze emotional intensity
- Generate personalized recommendations
- Track historical emotion patterns
- Learn from recommendation feedback
- Provide search, filtering, and reporting features
- Present results through an interactive dashboard

## Supported Emotions

The project works with six major emotions:

- Joy
- Sadness
- Anger
- Fear
- Surprise
- Disgust

## Project Milestones

### Milestone 1 – Sentiment Analysis

- Text input and file-based text ingestion
- Text preprocessing
- Sentiment analysis using VADER
- Basic Flask application

### Milestone 2 – Deep Emotion Classification

- Emotion dataset preparation
- Emotion classification
- BERT-based emotion classification
- DistilBERT-based emotion classification
- Confidence-based emotion prediction
- Six emotion categories

### Milestone 3 – Intelligent Recommendations

- Emotion intensity analysis
- Emotional state detection
- Dominant emotion detection
- Multiple emotion detection
- Positive/negative/mixed polarity
- Emotion severity analysis
- Personalized recommendations
- Hybrid recommendation engine
- Recommendation ranking
- Emotion history tracking
- Feedback-based recommendation improvement
- Recommendation explanations

### Milestone 4 – Dashboard and Reporting

- Interactive Streamlit dashboard
- Emotion trend analysis
- Daily, weekly, and monthly trends
- Recommendation history
- Recommendation feedback history
- Like/Dislike feedback
- Search and filtering
- Recommendation ranking display
- CSV report export
- PDF report export
- Automated testing
- Final dashboard validation

**Milestone 4 is the final milestone of this project.**

## Technologies Used

- Python
- Flask
- Streamlit
- Pandas
- VADER Sentiment
- BERT
- DistilBERT
- Transformers
- PyTorch
- Pytest
- JSON
- CSV
- PDF reporting
- Git
- GitHub

## Project Structure

```text
Sentiment_emotion_project/
│
├── milestone1/
│   ├── ingestion.py
│   ├── preprocessing.py
│   └── sentiment/
│
├── milestone2/
│   ├── data/
│   ├── emotion classification
│   └── model training files
│
├── milestone3/
│   ├── emotion_analysis/
│   ├── recommendation/
│   ├── hybrid/
│   ├── ranking/
│   └── tests/
│
├── milestone4/
│   ├── dashboard/
│   │   └── app.py
│   │
│   ├── data/
│   │   ├── history.py
│   │   ├── trend.py
│   │   ├── trend_chart.py
│   │   ├── feedback_history.py
│   │   ├── recommendation_history.py
│   │   └── search_filter.py
│   │
│   ├── reports/
│   │   └── export_reports.py
│   │
│   └── tests/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore