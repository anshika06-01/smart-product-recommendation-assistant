"""
Explanation Generator

Generates human-readable explanations describing why
a product was recommended to the user.
"""


class ExplanationGenerator:
    """
    Creates recommendation explanations based on
    the user's preferences and product attributes.
    """

    def generate(self, product, entities):
        """
        Generate reasons for recommending a product.

        Parameters:
            product (Series): Product details.
            entities (dict): Extracted user preferences.

        Returns:
            list: List of explanation strings.
        """

        reasons = []

        # Brand match
        if (
            entities.get("brand")
            and str(product["brand"]).lower() == entities["brand"].lower()
        ):
            reasons.append(
                f"✔ Matches your preferred brand: {entities['brand']}."
            )

        # Budget match
        if (
            entities.get("max_price")
            and product["discounted_price"] <= entities["max_price"]
        ):
            reasons.append(
                f"✔ Fits within your budget of ₹{entities['max_price']:,}."
            )

        # Rating match
        if entities.get("min_rating"):

            if product["rating"] >= entities["min_rating"]:

                reasons.append(
                    f"✔ Rating of {product['rating']:.1f} meets your minimum requirement."
                )

        else:

            reasons.append(
                f"✔ Highly rated product ({product['rating']:.1f} ⭐)."
            )

        # Default explanation
        if not reasons:
            reasons.append(
                "✔ Recommended based on your search preferences."
            )

        return reasons
