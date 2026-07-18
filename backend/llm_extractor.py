"""
LLM-based Entity Extractor

This module uses Google's Gemini model to extract structured
shopping entities from a user's natural language query.
"""

import json
from google import genai

from backend.config import GOOGLE_API_KEY, LLM_MODEL

class LLMExtractor:
    """
    Extracts shopping-related entities using Gemini.
    """

    def __init__(self):
        """Initialize the Gemini client."""
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def extract(self, query):
        """
        Extract shopping entities from a user query.

        Parameters:
            query (str): User's shopping query.

        Returns:
            dict: Extracted entities.
        """

        prompt = f"""
You are an AI shopping assistant.

Extract the following entities from the user's query.

Return ONLY valid JSON.

Fields:
- brand
- category
- subcategory
- max_price
- min_rating

If any field is missing, return null.

Example:

User:
Samsung mobile under 30k

Output:
{{
    "brand": "Samsung",
    "category": null,
    "subcategory": "Smartphone",
    "max_price": 30000,
    "min_rating": null
}}

User Query:
{query}
"""

        try:

            response = self.client.models.generate_content(
                model=LLM_MODEL,
                contents=prompt
            )

            text = response.text.strip()

            # Remove Markdown formatting if present
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "").strip()
            elif text.startswith("```"):
                text = text.replace("```", "").strip()

            return json.loads(text)

        except json.JSONDecodeError:
            print("Error: Gemini returned invalid JSON.")
            return None

        except Exception as error:
            print(f"Gemini API Error: {error}")
            return None
