import pandas as pd
from .constants import DAILY_RISK_FREE_RATE


def DailySharpeRatio(stockDF: pd.DataFrame) -> pd.DataFrame:
    stockDF["DailySharpeRatio"] = 0

    stockDF = stockDF.reset_index()

    print(stockDF.head())

    for i, row in stockDF.iterrows():
        nextIndex = int(i) + 1
        subset = stockDF.iloc[0:nextIndex]
        average_daily_return = (subset["DailyReturn"] * 0.01).mean()
        average_volatility = (subset["DailyReturn"] * 0.01).std()
        print(
            f"Return: {average_daily_return} | Volatility: {average_volatility} | RFR: {DAILY_RISK_FREE_RATE}"
        )

        sharpe_ratio = (
            average_daily_return - DAILY_RISK_FREE_RATE
        ) / average_volatility

        stockDF.loc[i, "DailySharpeRatio"] = sharpe_ratio

    stockDF = stockDF.set_index("Date")

    return stockDF
