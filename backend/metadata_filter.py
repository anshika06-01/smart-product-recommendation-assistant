import pandas as pd


class MetadataFilter:

    def __init__(self, dataset_path):
        """
        Load the dataset once when the class is created.
        """

        self.df = pd.read_csv(dataset_path)

    def filter_products(self, entities):

        filtered_df = self.df.copy()

        # -------------------------------
"""
Metadata Filtering Module

Filters products based on the entities extracted
from the user's natural language query.
"""

import pandas as pd


class MetadataFilter:
    """
    Filters the product dataset using metadata such as
    brand, category, subcategory, price, and rating.
    """

    def __init__(self, dataset_path):
        """
        Load the product dataset.

        Parameters:
            dataset_path (str): Path to the product dataset.
        """
        self.df = pd.read_csv(dataset_path)

    def filter_products(self, entities):
        """
        Filter products based on extracted entities.

        Parameters:
            entities (dict): Extracted entities from Gemini.

        Returns:
            pandas.DataFrame: Filtered products.
        """

        filtered_df = self.df.copy()

        # Filter by brand
        if entities.get("brand"):
            filtered_df = filtered_df[
                filtered_df["brand"].str.lower() == entities["brand"].lower()
            ]

        # Filter by category
        if entities.get("category"):
            filtered_df = filtered_df[
                filtered_df["category"].str.lower() == entities["category"].lower()
            ]

        # Filter by subcategory
        if entities.get("subcategory"):
            filtered_df = filtered_df[
                filtered_df["subcategory"].str.lower() == entities["subcategory"].lower()
            ]

        # Filter by maximum price
        if entities.get("max_price"):
            filtered_df = filtered_df[
                filtered_df["discounted_price"] <= entities["max_price"]
            ]

        # Filter by minimum rating
        if entities.get("min_rating"):
            filtered_df = filtered_df[
                filtered_df["rating"] >= entities["min_rating"]
            ]

        # Keep only products that are in stock
        filtered_df = filtered_df[
            filtered_df["stock_status"].str.lower() == "in stock"
        ]

        return filtered_df.reset_index(drop=True)        # Brand Filter
        # -------------------------------
        if entities["brand"]:

            filtered_df = filtered_df[
                filtered_df["brand"].str.lower()
                == entities["brand"].lower()
            ]

        # -------------------------------
        # Category Filter
        # -------------------------------
        if entities["category"]:

            filtered_df = filtered_df[
                filtered_df["category"].str.lower()
                == entities["category"].lower()
            ]

        # -------------------------------
        # Subcategory Filter
        # -------------------------------
        if entities["subcategory"]:

            filtered_df = filtered_df[
                filtered_df["subcategory"].str.lower()
                == entities["subcategory"].lower()
            ]

        # -------------------------------
        # Budget Filter
        # -------------------------------
        if entities["max_price"]:

            filtered_df = filtered_df[
                filtered_df["discounted_price"]
                <= entities["max_price"]
            ]

        # -------------------------------
        # Rating Filter
        # -------------------------------
        if entities["min_rating"]:

            filtered_df = filtered_df[
                filtered_df["rating"] >= entities["min_rating"]
            ]
            
        # -------------------------------
        # Stock Filter
        # -------------------------------
        filtered_df = filtered_df[
            filtered_df["stock_status"].str.lower() == "in stock"
        ]

        return filtered_df
