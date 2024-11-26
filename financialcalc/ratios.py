from typing import cast
import pandas as pd
from .constants import DAILY_RISK_FREE_RATE


def DailySharpeRatio(stockDF: pd.DataFrame) -> pd.DataFrame:
    stockDF["DailySharpeRatio"] = 0

    stockDF = stockDF.reset_index()

    for i, _ in stockDF.iterrows():
        i = cast(int, i)
        nextIndex = i + 1
        subset = stockDF.iloc[0:nextIndex]
        average_daily_return = (subset["DailyReturn"] * 0.01).mean()
        average_volatility = (subset["DailyReturn"] * 0.01).std()

        sharpe_ratio = (
            average_daily_return - DAILY_RISK_FREE_RATE
        ) / average_volatility

        stockDF.loc[i, "DailySharpeRatio"] = sharpe_ratio

    stockDF = stockDF.set_index("Date")

    return stockDF
