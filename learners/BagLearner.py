from typing import Any, Type, cast
from learners.DTLearner import DTLearner
from learners.RTLearner import RTLearner
import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    recall_score,
    root_mean_squared_error,
    mean_absolute_error,
    precision_score,
    f1_score,
)


class BagLearner:
    def __init__(
        self,
        learner: Type[DTLearner],
        bags: int,
        classifier=False,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Constructor for BagLearner.
        Defines an array that contains each learner.
        Parameters:
            learner (Type[DTLearner]): The type of learner to bag.
            bags (int): The number of bags to create.
            classifier (boolena=False): Whether the BagLearner is a classification model.
            *args (Any): Unspecified arguments to pass to the learners.
            **kwargs (Any): Keyworded arguments to pass to the learners.
        Returns:
            None
        """
        self.learners = [
            learner(classifier=classifier, *args, **kwargs) for _ in range(bags)
        ]
        self.classifier = classifier

    def add_evidence(self, dataX: pd.DataFrame, dataY: pd.Series) -> None:
        """Creates a new subset of feature and target data for each learner.
        Then trains each learner.
        Parameters:
            dataX (pd.DataFrame): Feature matrix for training.
            dataY (pd.Series): Target values for training.
        Returns:
            None
        """
        for learner in self.learners:
            random_indexes = dataX.sample(n=len(dataX), replace=True).index

            sampled_dataX = dataX.loc[random_indexes]

            sampled_dataY = dataY[random_indexes]

            sampled_dataX = cast(pd.DataFrame, sampled_dataX)
            sampled_dataY = cast(pd.Series, sampled_dataY)

            sampled_dataX = sampled_dataX.reset_index()

            sampled_dataX = sampled_dataX.drop(["Date"], axis=1)

            target_label = sampled_dataY.name

            sampled_dataY = sampled_dataY.reset_index().pop(target_label)

            learner.add_evidence(sampled_dataX, sampled_dataY)

    def query(self, points: list[dict]) -> np.ndarray:
        """Make predictions for given input points.
        Parameters:
            points (list[dict]): Data points to predict.
        Returns:
            numpy.ndarray: Predicted values for the input data.
        """

        predictions = np.array([learner.query(points) for learner in self.learners])

        if self.classifier:
            most_common = mode(predictions, axis=0).mode
            return most_common

        averaged_predictions = np.mean(predictions, axis=0)

        return averaged_predictions

    def generate_regression_stats(
        self, y_true: pd.Series, y_pred: np.ndarray
    ) -> tuple[float, float]:
        """Generates statistics relevant to a regression model.
        Parameters:
            y_true (pd.Series): The true values of the target.
            y_pred (np.ndarray): The predicted values of the target.
        Returns:
            tuple[float, float]: Root Mean Squared Error, Mean Absolute Error
        """
        return root_mean_squared_error(y_true, y_pred), mean_absolute_error(
            y_true, y_pred
        )

    def generate_classification_stats(
        self, y_true: pd.Series, y_pred: np.ndarray
    ) -> tuple[float, float, float, float, np.ndarray]:
        """Generates statistics relevant to a classification mode.
        Parameters:
            y_true (pd.Series): The true values of the target.
            y_pred (np.ndarray): The predicted values of the target.
        Returns:
            tuple[float, float, float, np.ndarray]: Accuracy Score, Precision Score, F1 Score, Recall Score Confusion Matrix
        """

        return (
            accuracy_score(y_true, y_pred),
            precision_score(y_true, y_pred, average="weighted"),
            f1_score(y_true, y_pred, average="weighted"),
            recall_score(y_true, y_pred, average="weighted"),
            confusion_matrix(y_true, y_pred),
        )
