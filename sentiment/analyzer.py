import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Ensure the VADER lexicon is downloaded (only needs to be done once)
# IF YOU'RE DOWNLOADING THIS, MAKE SURE TO RUN IT AT LEAST ONCE!!!!
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))
nltk.download("vader_lexicon", download_dir=os.path.join(os.path.dirname(__file__), "nltk_data"))

def evaluate_sentiment(article_text: str) -> int:
    """
    Evaluate the sentiment of a given article text on a scale of 1-10.
    Args:
        article_text (str): The article content.
    Returns:
        int: Sentiment score on a scale of 1-10, reflecting a negative-positive sentiment scale.
    """
    # Initialize the Sentiment Intensity Analyzer
    sia = SentimentIntensityAnalyzer()

    # Analyze the sentiment
    sentiment = sia.polarity_scores(article_text)

    # Scale compound score (-1 to 1) to a 1-10 range
    compound_score = sentiment["compound"]
    scaled_score = int(((compound_score + 1) / 2) * 9 + 1)  # Scale to 1–10

    return scaled_score
