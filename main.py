import os
import sys
from builder.builder import Builder
from learners import BagLearner, DTLearner, RTLearner, split_time_series
from json import loads
from typing import cast
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from typing import cast
import numpy as np
from rich import print
import pyfiglet
import os
import seaborn as sns
from matplotlib import pyplot as plt

DATASET_LOADED = False
DATASET: pd.DataFrame = pd.DataFrame()


def clear_console():
    """Clears console, uses 'cls' if OS is Windows,
    otherwise uses 'clear'."""
    os.system("cls" if os.name == "nt" else "clear")


def splash_screen():
    """Clears the console and prints a nice splash
    screen, including the names of authors."""
    clear_console()
    f = pyfiglet.figlet_format("SDSP", font="slant")
    print(f"[white]{f}[/white]")
    print("[white]2024, Venn Reddy & Stephen Sulimani[/white]")
    print()


def create_dataset():
    """Walks a user through the process of creating a
    new dataset and saving it."""
    global DATASET_LOADED
    global DATASET
    splash_screen()
    print("[bold bright_yellow]Please enter a stock ticker[/bold bright_yellow]")
    ticker = input().upper()

    splash_screen()
    print("[bold bright_yellow]Please enter a start date[/bold bright_yellow]")
    print("[italic yellow]01-02-2024 -> January 2, 2024[/italic yellow]")
    start_date = input()

    splash_screen()
    print("[bold bright_yellow]Please enter an end date[/bold bright_yellow]")
    print("[italic yellow]01-02-2024 -> January 2, 2024[/italic yellow]")
    end_date = input()

    splash_screen()
    print(
        "[bold bright_yellow]Please enter your desired return threshold[/bold bright_yellow]"
    )
    print("[italic yellow]0.5 -> 0.5%[/italic yellow]")
    threshold = float(input())

    splash_screen()

    DATASET = Builder.build(ticker, start_date, end_date, threshold)
    DATASET_LOADED = True

    print(
        "[bold bright_yellow]Your dataset is complete, please press any key to continue.[/bold bright_yellow]"
    )
    input()

    splash_screen()

    print(
        "[bold bright_yellow]Please enter a path to save your dataset.[/bold bright_yellow]"
    )
    save_path = input()

    if not save_path.endswith(".csv"):
        save_path = f"{save_path}.csv"

    DATASET.to_csv(save_path)

    splash_screen()

    print(
        f"[bold bright_yellow]Your dataset has been saved at {save_path}[/bold bright_yellow]"
    )
    print(
        "[bold bright_yellow]Please press any key to return to the main menu[/bold bright_yellow]"
    )
    input()


def load_dataset():
    """Walks a user through the process of loading a
    dataset."""
    global DATASET
    global DATASET_LOADED

    error = ""

    while True:
        splash_screen()

        if error != "":
            print(f"[bold red]{error}[/bold red]")
            print()
            error = ""

        print(
            "[bold bright_yellow]Please enter the path for your previously created dataset[/bold bright_yellow]"
        )
        dataset_path = input()

        try:
            DATASET = pd.read_csv(dataset_path)
            DATASET["Date"] = pd.to_datetime(DATASET["Date"])
            DATASET = DATASET.set_index("Date")
            if len(DATASET) == 0:
                error = "There are no rows in the dataset."
                continue
        except:
            error = "Your dataset was unable to be read."
            continue
        DATASET_LOADED = True
        return


def train_model():
    """Walks a user through the process of training
    a model."""
    global DATASET
    global DATASET_LOADED

    splash_screen()

    if not DATASET_LOADED:
        print("[bold red]A dataset must be loaded to train a model.[/bold red]")
        return

    print("[bold bright_yellow]Please select from the menu below:[/bold bright_yellow]")
    print()
    print("[italic yellow]1 - Decision Tree Learners[/italic yellow]")
    print("[italic yellow]2 - Random Tree Learners[/italic yellow]")
    selection = int(input())

    splash_screen()

    print(
        "[bold bright_yellow]How many learners should be used in the BagLearner?[/bold bright_yellow]"
    )
    learner_count = int(input())

    splash_screen()

    print("[bold bright_yellow]Now training...[/bold bright_yellow]")

    encoder = LabelEncoder()
    DATASET["Signal"] = encoder.fit_transform(DATASET["Signal"])

    label_mapping = {
        label: index for index, label in enumerate(cast(np.ndarray, encoder.classes_))
    }

    print(f"[italic yellow]Label Encoder Classes: {label_mapping}[/italic yellow]")

    train_x, train_y, test_x, test_y = split_time_series(DATASET)

    print(f"[italic yellow]Train Set Length: {len(train_x)}[/italic yellow]")
    print(f"[italic yellow]Test Set Length: {len(test_x)}[/italic yellow]")

    print(f"[italic yellow]Train Set Head[/italic yellow]")
    print(train_x.head())

    learner = BagLearner(RTLearner, 50, True)

    if selection == 1:
        learner = BagLearner(DTLearner, learner_count, True)
    else:
        learner = BagLearner(RTLearner, learner_count, True)

    learner.add_evidence(train_x, train_y)

    print("[bold bright_green]Training Complete![/bold bright_green]")
    print("[bold bright_yellow]Now testing...[/bold bright_yellow]")

    y_pred = learner.query(loads(cast(str, test_x.to_json(orient="records"))))

    accuracy, precision, f1, recall, confusion = learner.generate_classification_stats(
        test_y, y_pred
    )

    print("[bold bright_green]Testing Complete![/bold bright_green]")

    print("[italic green]Test Results[/italic green]")
    print(f"[italic green]Accuracy: {accuracy}[/italic green]")
    print(f"[italic green]Precision: {precision}[/italic green]")
    print(f"[italic green]F1 Score: {f1}[/italic green]")
    print(f"[italic green]Recall: {recall}[/italic green]")
    plt.figure(figsize=confusion.shape)
    sns.heatmap(
        confusion,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=np.unique(test_y),
        yticklabels=np.unique(test_y),
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    plt.show()
    input()


error = ""

while True:
    splash_screen()

    if DATASET_LOADED:
        print(
            f"[bold bright_green]Loaded Dataset: {len(DATASET)} rows[/bold bright_green]"
        )

    print("[bold bright_yellow]Please select from the menu below:[/bold bright_yellow]")
    print()

    if error != "":
        print(f"[bold red]{error}[/bold red]")
        print()
        error = ""

    print("[italic yellow]1 - Create a Dataset[/italic yellow]")
    print("[italic yellow]2 - Load a Dataset[/italic yellow]")
    print("[italic yellow]3 - Train and Test a Model[/italic yellow]")

    selection = 0

    try:
        raw_response = input()

        if raw_response.upper() == "Q":
            break

        selection = int(raw_response)
        if selection > 3 or selection < 1:
            error = "Your selection was invalid."
            continue
    except:
        error = "Your selection must be a valid integer."
        continue

    if selection == 1:
        create_dataset()
    elif selection == 2:
        load_dataset()
    elif selection == 3:
        train_model()
