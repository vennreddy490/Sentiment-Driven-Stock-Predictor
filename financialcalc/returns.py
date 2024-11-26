import pandas as pd


def DailyReturn(stockDF: pd.DataFrame) -> pd.DataFrame:
    """Creates a new column called DailyReturn, to calculate
    the return for each day, or row of the column, from previous
    day's close, to current day's close.

    Args:
        stockDF (pd.DataFrame): The DataFrame representing the stocks historical performance.

    Returns:
        pd.DataFrame: The amended DataFrame containing the DailyReturn column.
    """

    # Calculate Daily Return As A Percentage
    stockDF["DailyReturn"] = (
        (stockDF["Close"] - stockDF["Close"].shift(1)) / stockDF["Close"].shift(1) * 100
    )

    stockDF = stockDF.dropna(how="any")

    return stockDF


def BuySellHold(stockDF: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Creates a new column called Signal, to determine whether the proper
    decision (when looking at the next day's close price) was to buy, sell,
    or hold, depending on the movement in price, as a percentage, with a
    specified threshold.
    If the next days daily return is greater than the threshold, it signals
    a buy (B). If the next days daily return is less than the threshold times
    negative 1, it signals a sell (S). Otherwise, it signals a hold (H).

    Args:
        stockDF (pd.DataFrame): The DataFrame representing the stocks historical performance.

    Returns:
        pd.DataFrame: The amended DataFrame containing the Signal column.
    """
    stockDF["Signal"] = (
        stockDF["DailyReturn"]
        .shift(-1)
        .apply(
            lambda x: "B" if x > threshold else ("S" if x < (-1 * threshold) else "H")
        )
    )

    stockDF = stockDF.dropna(how="any")

    return stockDF
