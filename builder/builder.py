from financialcalc.returns import BuySellHold, DailyReturn
from financialcalc.ratios import DailySharpeRatio
from godel.godel import Godel
from sentiment.analyzer import create_sentiment_column
from stooq import Stooq
from datetime import datetime
import pandas as pd
from multiprocessing.pool import ThreadPool


class Builder:
    def __init__(self):
        pass

    @staticmethod
    def build(
        ticker: str, startDate: str, endDate: str, threshold: float, threads: int = 250
    ) -> pd.DataFrame:
        """Takes in a ticker, start and end dates, and builds
        a complete dataset, including financial statistics and
        sentiment analysis data. Returns a DataFrame that is
        ready to be used for training and testing.
        start/endDate format: 09-20-2003 -> September 20, 2003

        Args:
            ticker (str): The ticker to build the dataset for.
            startDate (str): The start date to begin looking for data.
            endDate (str): The cutoff date to stop looking for data.
            threshold (float): Threshold for a Daily Return Percent to be
                            considered a BUY, SELL, or HOLD. Must be a
                            positive floating point number.
            threads (int): Number of threads to use when pulling article text, defaults to 250.

        Returns:
            pd.DataFrame: The DataFrame representing the stock dataset.
        """

        start_date = datetime.strptime(startDate, "%M-%d-%Y")
        end_date = datetime.strptime(endDate, "%M-%d-%Y")

        stock_df = Stooq.download(
            ticker, start_date.strftime("%Y%M%d"), end_date.strftime("%Y%M%d")
        )

        if len(stock_df) == 0:
            raise ValueError(f"No data loaded for ticker: {ticker}.")

        print(f"[BUILDER] {ticker} DATA LOADED")
        # Checkpoint: Valid DataFrame of historical
        #             stock data has been created.

        stock_df = DailyReturn(stock_df)
        stock_df = BuySellHold(stock_df, threshold)
        stock_df = DailySharpeRatio(stock_df)

        if any(
            col not in stock_df.columns
            for col in ["DailyReturn", "Signal", "DailySharpeRatio"]
        ):
            raise ValueError(
                f"A financial statistic calculation didn't work for ticker: {ticker}."
            )

        print(f"[BUILDER] {ticker} FINANCIAL STATS CALCULATED")
        # Checkpoint: Financial Statistics Calculated
        #             and added to DataFrame.

        articles = Godel.queryNews(
            [ticker], start_date.strftime("%M-%d-%Y"), end_date.strftime("%M-%d-%Y")
        )

        articles = articles[ticker]

        if len(articles) == 0:
            raise ValueError(f"No articles were fetched for ticker: {ticker}.")

        print(f"[BUILDER] {ticker} NEWS ARTICLES FOUND: {len(articles)}")

        # Checkpoint: Articles pulled for given ticker.

        pool = ThreadPool(threads)

        for article in articles:
            pool.apply_async(article.pullArticle, args=())
        pool.close()
        pool.join()

        # Filters articles where text could not be retrieved
        parsedArticles = [
            article for article in articles if article.articleText is not None
        ]

        print(f"[BUILDER] {ticker} ARTICLES PARSED: {len(parsedArticles)}")

        stock_df = create_sentiment_column(stock_df, parsedArticles)

        print(f"[BUILDER] {ticker} SENTIMENT ANALYZED")

        stock_df = stock_df.dropna(how="any")

        print(f"[BUILDER] {ticker} NA ROWS DROPPED")

        return stock_df
