from typing import Any, List, cast
import pandas as pd
import numpy as np
from pandas.core.algorithms import nunique_ints

np.seterr(divide="ignore", invalid="ignore")


class DTLearner:
    def __init__(self, leaf_size=1, verbose=False, classifier=False):
        """Constructor"""
        self.leaf_size = leaf_size
        self.tree: List[str | float | List[str | float | List[Any]]] = []
        self.max_depth = 5
        self.classifier = classifier

    def build_tree(
        self, dataX: pd.DataFrame, dataY: pd.Series, depth=0
    ) -> List[str | float | List[str | float | List[Any]]]:
        """Recursively builds the decision tree.
        Parameters:
            dataX (pd.DataFrame): Feature matrix for training.
            dataY (pd.Series): Target values for training.
        Returns:
            List[str | float | List[str | float | List[Any]]]: The complete Decision Tree
        """

        if (depth >= self.max_depth or len(dataX) <= self.leaf_size) or (
            dataX.nunique().max() == 1 or dataY.nunique() == 1
        ):
            # Base Case Reached, Create Leaf Node
            if self.classifier:
                unique, counts = np.unique(dataY, return_counts=True)
                index = np.argmax(counts)
                most_common = unique[index]
                return [f"Leaf: {most_common}"]
            return [f"Leaf: {dataY.mean()}"]

        feature, split_val = self.select_split_feature(dataX, dataY)

        left_data = dataX[dataX[feature] <= split_val]

        left_target = dataY[left_data.index]

        right_data = dataX[dataX[feature] > split_val]
        right_target = dataY[right_data.index]

        # In the event that a split results in 0 data points on one of the subtrees
        if len(left_data) == 0 or len(right_data) == 0:
            if self.classifier:
                unique, counts = np.unique(dataY, return_counts=True)
                index = np.argmax(counts)
                most_common = unique[index]
                return [f"Leaf: {most_common}"]
            return [f"Leaf: {dataY.mean()}"]

        left_data = cast(pd.DataFrame, left_data)  # For Linting Purposes
        left_target = cast(pd.Series, left_target)  # For Linting Purposes
        right_data = cast(pd.DataFrame, right_data)  # For Linting Purposes
        right_target = cast(pd.Series, right_target)  # For Linting Purposes

        left_tree = self.build_tree(left_data, left_target, depth + 1)
        right_tree = self.build_tree(right_data, right_target, depth + 1)

        return [feature, split_val, left_tree, right_tree]

    def add_evidence(self, dataX: pd.DataFrame, dataY: pd.Series):
        """Train the model with provided data.
        Parameters:
            data_x (numpy.ndarray): Feature matrix for training.
            data_y (numpy.ndarray): Target values for training.
        Returns:
            None
        """
        self.tree = self.build_tree(dataX, dataY)

    def query(self, points: list[dict]) -> np.ndarray:
        """Make predictions for given input points.
        Parameters:
            points (list[dict]): Data points to predict.
        Returns:
            numpy.ndarray: Predicted values for the input data.
        """
        predictions = []

        for point in points:
            tree = self.tree
            while True:
                if isinstance(cast(list, tree)[0], str) and cast(
                    str, tree[0]
                ).startswith("Leaf:"):
                    break

                tree = cast(
                    List[str | float | List[str | float | List[Any]]], tree
                )  # For Linting Purposes
                feature = cast(str, tree[0])  # For Linting Purposes
                split_val = cast(float, tree[1])  # For Linting Purposes

                if point[feature] <= split_val:
                    # Move Left
                    tree = tree[2]
                else:
                    # Move Right
                    tree = tree[3]

            predictions.append(
                float(cast(str, cast(list, tree)[0]).replace("Leaf: ", ""))
            )

        return np.array(predictions, dtype=float)

    def select_split_feature(
        self, dataX: pd.DataFrame, dataY: pd.Series
    ) -> tuple[str, float]:
        """Select the best feature based on correlation between feature and target.
        Ties broken based on alphabetical order.
        Parameters:
            dataX (pd.DataFrame): Feature matrix for training.
            dataY (pd.DataFrame): Target values for training.
        Returns:
            tuple[str, float]: Feature label, split value
        """

        correlations = dataX.apply(lambda x: x.corr(dataY))

        correlations = cast(pd.DataFrame, correlations)  # For Linting Purposes

        tied_features = correlations[
            correlations.abs() == correlations.abs().max()
        ].index.tolist()

        # Alphabetical Tie Breaking

        sorted_features = sorted(tied_features)

        # print(sorted_features)

        best_feature = sorted_features[0]

        # Splitting Data by Median

        split_val = dataX[best_feature].median()

        split_val = cast(float, split_val)  # For Linting Purposes
        best_feature = cast(str, best_feature)  # For Linting Purposes

        return best_feature, split_val
