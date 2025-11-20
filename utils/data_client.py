from pathlib import Path

import pandas as pd


class DataClient:
    def __init__(self):
        self.path = Path.cwd()
        self.df_query = pd.read_parquet(
            self.path / "data/shopping_queries_dataset_examples.parquet"
        )
        self.df_product = pd.read_parquet(
            self.path / "data/shopping_queries_dataset_products.parquet"
        )
        self.df_examples_products = pd.merge(
            self.df_query,
            self.df_product,
            how="left",
            left_on=["product_locale", "product_id"],
            right_on=["product_locale", "product_id"],
        )
        self.queries = [
            "aa batteries 100 pack",
            "kodak photo paper 8.5 x 11 glossy",
            "dewalt 8v max cordless screwdriver kit, gyroscopic",
        ]

    def get_data(self):
        df = self.df_examples_products[
            (self.df_examples_products["esci_label"].str.strip() == "E")
            & (self.df_examples_products["query"].isin(self.queries))
        ][["query", "product_title"]].reset_index(drop=True)

        return df


def preprocess_data():
    return DataClient().get_data()
