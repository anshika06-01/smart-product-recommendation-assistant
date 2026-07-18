"""
Recommendation Engine

Ranks filtered products using a weighted scoring system
based on rating, popularity, reviews, and price.
"""

import pandas as pd


class Recommender:
    """
    Generates the top product recommendations.
    """

    def recommend(self, filtered_df, top_n=3):
        """
        Rank products and return the top recommendations.

        Parameters:
            filtered_df (DataFrame): Products after metadata filtering.
            top_n (int): Number of recommendations to return.

        Returns:
            DataFrame: Top recommended products.
        """

        # Return immediately if no products match
        if filtered_df.empty:
            return filtered_df

        df = filtered_df.copy()

        # Normalize rating
        df["rating_score"] = df["rating"] / df["rating"].max()

        # Normalize review count
        df["review_score"] = (
            df["reviews_count"] / df["reviews_count"].max()
        )

        # Normalize popularity
        df["popularity_score_norm"] = (
            df["popularity_score"] / df["popularity_score"].max()
        )

        # Normalize price
        # Lower price results in a higher score
        df["price_score"] = (
            1 - (
                df["discounted_price"] /
                df["discounted_price"].max()
            )
        )

        # Weighted recommendation score
        df["final_score"] = (
            0.40 * df["rating_score"] +
            0.30 * df["popularity_score_norm"] +
            0.20 * df["review_score"] +
            0.10 * df["price_score"]
        )

        # Sort by final score
        df = df.sort_values(
            by="final_score",
            ascending=False
        )

        return df.head(top_n).reset_index(drop=True)
