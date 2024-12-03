import os
import pandas as pd
from financialcalc.returns import DailyReturn, BuySellHold
from financialcalc.ratios import DailySharpeRatio
from godel import Godel, Article, articleSerializer
from import_stock_data import get_data_yf_symbol, symbol_to_path
import json
from sentiment.analyzer import evaluate_sentiment


def main():
    # Step 1: Define stock tickers and timeframe
    tickers_file = "Symbols_To_Import.csv"  # CSV file with the stock tickers
    tickers_df = pd.read_csv(tickers_file)
    tickers = tickers_df["Symbol"].tolist()

    start_date = "2024-01-01"  # Example: January 1, 2024
    end_date = "2024-11-28"  # Example: November 28, 2024
    threshold = 2.0  # Threshold for Buy/Sell signals (percentage)

    # Step 2: Ensure "data" directory exists
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)

    # Step 3: Retrieve and process historical data
    all_historical_data = {}
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        data = get_data_yf_symbol(ticker, start_date, end_date)
        if not data.empty:
            data.to_csv(symbol_to_path(ticker, base_dir=data_dir))
            data = DailyReturn(data)
            data = BuySellHold(data, threshold)
            data = DailySharpeRatio(data)
            all_historical_data[ticker] = data
            file_path = os.path.join(data_dir, f"{ticker}.csv")
            data.to_csv(file_path)
            print(f"Saved historical data for {ticker} at {file_path}.")
        else:
            print(f"No data found for {ticker}.")

    # Step 4: Fetch and process news articles
    print("Fetching news articles...")
    godel = Godel()
    news_articles = godel.queryNews(tickers, "01-01-2024", "11-28-2024")

    # Read Each Article
    for _, articles in news_articles.items():
        for article in articles:
            article.pullArticle()

    # news_file_path = os.path.join(<SPECIFIED_DIRECTORY>, "news_articles.json")
    news_file_path = "news_articles.json"

    news_articles = json.dumps(news_articles, indent=4, default=articleSerializer)

    open(news_file_path, "w").write(news_articles)

    print(f"Saved news articles at {news_file_path}.")
    print("Data retrieval and storage complete.")

    # Step 5: Analyze Sentiment of Given Articles
    with open("articles/test_aapl_article.txt", "r", encoding="utf-8") as file:
        file_content = file.read().strip()
    test_string = file_content

    # Evaluate Sentiment:
    sentiment_score = evaluate_sentiment(test_string)
    print(f"Example 1 Sentiment score: {sentiment_score}")

    # Other examples:
    # Example 2:
    article_text = """
    Apple's new product launch has been met with widespread acclaim. Experts believe it
    will drive record-breaking sales, while customers praise its innovative features.
    """
    sentiment_score = evaluate_sentiment(article_text)
    print(f"Example 2 Sentiment Score: {sentiment_score}")

    # Example 3:
    article_text = """
    Boo Lame Apple sucks this is so bad for the market boo lame. 
    """
    sentiment_score = evaluate_sentiment(article_text)
    print(f"Example 3 Sentiment Score: {sentiment_score}")


if __name__ == "__main__":
    main()
