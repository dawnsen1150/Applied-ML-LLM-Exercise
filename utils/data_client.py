from pathlib import Path

import pandas as pd


class DataClient:
    def __init__(self):
        self.path = Path.cwd()
        self.df_examples_products = pd.read_csv(
            self.path / "data/shopping_queries_dataset_exercise.csv"
        )


def get_data():
    return DataClient().df_examples_products
