from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# Create VADER analyzer
analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text using VADER.

    Returns:
        positive score
        negative score
        neutral score
        compound score
        sentiment classification
    """

    if text is None or text.strip() == "":
        return None

    # Generate sentiment scores dynamically
    scores = analyzer.polarity_scores(text)

    compound = scores["compound"]

    # Classify sentiment using VADER compound score
    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {
        "positive": scores["pos"],
        "negative": scores["neg"],
        "neutral": scores["neu"],
        "compound": compound,
        "sentiment": sentiment
    }