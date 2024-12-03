from typing import Tuple
import pandas as pd


def split_time_series(
    df: pd.DataFrame, train_size: float = 0.8
) -> Tuple[pd.DataFrame, pd.Series, pd.DataFrame, pd.Series]:
    """
    Splits a time series dataframe into training and testing sets.

    Args:
        df (pd.DataFrame): The input time series dataframe.
        train_size (float): The proportion of the data to be used as the training set (default is 0.8 for 80%).

    Returns:
        pd.DataFrame, pd.DataFrame: The training set and testing set.
    """
    # Calculate the index for the split
    split_index = int(len(df) * train_size)

    # Split the dataframe into training and testing sets
    train_set = df.iloc[:split_index]

    train_y = train_set.pop("Signal")

    test_set = df.iloc[split_index:]

    test_y = test_set.pop("Signal")

    return train_set, train_y, test_set, test_y
