import os
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from godel import Article

# Ensure the VADER lexicon is downloaded (only needs to be done once)
# IF YOU'RE DOWNLOADING THIS, MAKE SURE TO RUN IT AT LEAST ONCE!!!!
nltk.data.path.append(os.path.join(os.path.dirname(__file__), "nltk_data"))
nltk.download(
    "vader_lexicon", download_dir=os.path.join(os.path.dirname(__file__), "nltk_data")
)


def evaluate_sentiment(article_text: str) -> float:
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

    compound_score = sentiment["compound"]
    # Scale compound score (-1 to 1) to a 1-10 range
    # scaled_score = int(((compound_score + 1) / 2) * 9 + 1)  # Scale to 1–10

    return compound_score


# def create_sentiment_column(stock_df: pd.DataFrame, articles: list[Article]) -> pd.DataFrame:
def create_sentiment_column(
    stock_df: pd.DataFrame, articles: list[Article]
) -> pd.DataFrame:
    """
    Evaluates the news for a stock ticker for a particular day, averages it, and appends the mean
    sentiment of that news to a new column called "Sentiment" for a stock ticker.
    Args:
        stock_df: The stock ticker and associated financial calculations, date-indexed.
        articles: The associated articles for a stock ticker.
    Returns:
        new_df: The resulting df with new "Sentiment" column added.
    """

    # Making sure date is in datetime format, and creating Sentiment column
    stock_df.index = pd.to_datetime(stock_df.index)
    stock_df["Sentiment"] = 0.0

    for date in stock_df.index:
        matching_articles = []

        # Loop through all the articles to find those that match the date, & append them.
        for article in articles:
            # article_date = pd.to_datetime(article['publicationTime']).date()
            article_date = pd.to_datetime(article.publicationTime).date()
            if article_date == date.date():
                matching_articles.append(article)

        # If there are matching articles, evaluate their sentiment and average them
        if matching_articles:
            # Debug Flag: Shows all the matching articles by date.
            # print(f"Matches found for date {date.date()}:")
            # print("\n".join(f"\tArticle: {article['title']}" for article in matching_articles))

            sentiments = []
            for article in matching_articles:
                sentiment = evaluate_sentiment(article.articleText)
                sentiments.append(sentiment)

            # Default case sentiment is 0, otherwise we update the sentiment.
            avg_sentiment = 0.0
            if sentiments:
                avg_sentiment = sum(sentiments) / len(sentiments)
            stock_df.at[date, "Sentiment"] = avg_sentiment

    return stock_df
