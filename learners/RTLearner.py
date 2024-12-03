from typing import cast
import numpy as np
import pandas as pd
from .DTLearner import DTLearner


class RTLearner(DTLearner):
    def select_split_feature(
        self, dataX: pd.DataFrame, dataY: pd.Series
    ) -> tuple[str, float]:
        """Randomly selects a feature, and splits the data
        based on median.
        Parameters:
            dataX (pd.DataFrame): Feature matrix for training.
            dataY (pd.DataFrame): Target values for training.
        Returns:
            tuple[str, float]: Feature label, split value
        """
        # Randomly Select Feature
        feature = dataX.columns.to_series().sample(n=1).iloc[0]

        # Splitting Data by Median

        split_val = dataX[feature].median()

        split_val = cast(float, split_val)  # For Linting Purposes
        feature = cast(str, feature)  # For Linting Purposes

        return feature, split_val
