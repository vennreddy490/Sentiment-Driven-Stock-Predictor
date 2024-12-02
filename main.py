import os
import pandas as pd
from financialcalc.returns import DailyReturn, BuySellHold
from financialcalc.ratios import DailySharpeRatio
from godel import Godel
from import_stock_data import get_data_yf_symbol, symbol_to_path
import json

def main():
    # Step 1: Define stock tickers and timeframe
    tickers_file = "Symbols_To_Import.csv"  # CSV file with the stock tickers
    tickers_df = pd.read_csv(tickers_file)
    tickers = tickers_df["Symbol"].tolist()

    start_date = "2024-01-01"  # Example: January 1, 2024
    end_date = "2024-11-28"    # Example: November 28, 2024
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
    # news_file_path = os.path.join(<SPECIFIED_DIRECTORY>, "news_articles.json")
    news_file_path = "news_articles.json"
    with open(news_file_path, "w") as json_file:
        json.dump(
            {ticker: [article.__dict__ for article in articles]
             for ticker, articles in news_articles.items()},
            json_file,
            indent=4
        )
    print(f"Saved news articles at {news_file_path}.")

    print("Data retrieval and storage complete.")

if __name__ == "__main__":
    main()
