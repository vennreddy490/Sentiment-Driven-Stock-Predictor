import os
from builder.builder import Builder
from learners import BagLearner, DTLearner, RTLearner, split_time_series
from json import loads
from typing import cast
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from typing import cast
import numpy as np

stock_data: pd.DataFrame = pd.DataFrame()

stock_data = Builder.build("AAPL", "01-01-2024", "12-01-2024", 0.5, 500)
stock_data.to_csv("data/AAPL.csv")


# if not os.path.exists("data/AAPL.csv"):
#     aapl_data = Builder.build("AAPL", "01-01-2024", "12-01-2024", 0.5, 500)
#     aapl_data.to_csv("data/AAPL.csv")
# else:
#     aapl_data = pd.read_csv("data/AAPL.csv")
#     aapl_data["Date"] = pd.to_datetime(aapl_data["Date"])
#     aapl_data = aapl_data.set_index("Date")

encoder = LabelEncoder()
stock_data["Signal"] = encoder.fit_transform(stock_data["Signal"])

label_mapping = {
    label: index for index, label in enumerate(cast(np.ndarray, encoder.classes_))
}


print(f"Label Encoder Classes: {label_mapping}")

train_x, train_y, test_x, test_y = split_time_series(stock_data)

print(f"Train Set Length: {len(train_x)}")
print(f"Test Set Length: {len(test_x)}")

print(f"Train Set Head")
print(train_x.head())

print(f"Train Y Head")
print(train_y.head())

learner = BagLearner(RTLearner, 50, True)

learner.add_evidence(train_x, train_y)

print("Successfully Trained")

y_pred = learner.query(loads(cast(str, test_x.to_json(orient="records"))))

accuracy, precision, f1, recall, _ = learner.generate_classification_stats(
    test_y, y_pred
)

print("Test Results")
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"F1 Score: {f1}")
print(f"Recall: {recall}")
