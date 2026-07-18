"""
AI Response Generator

Generates a natural language response based on the
user's shopping query and extracted entities.
"""

from google import genai

from backend.config import GOOGLE_API_KEY, LLM_MODEL


class ResponseGenerator:
    """
    Generates a conversational response using Gemini.
    """

    def __init__(self):
        """Initialize the Gemini client."""
        self.client = genai.Client(api_key=GOOGLE_API_KEY)

    def generate(self, query, entities):
        """
        Generate a friendly response for the user.

        Parameters:
            query (str): Original user query.
            entities (dict): Extracted shopping entities.

        Returns:
            str: AI-generated response.
        """

        prompt = f"""
You are an AI shopping assistant.

The user asked:

{query}

The extracted entities are:

{entities}

Write a friendly response in 2-3 sentences.

Do NOT recommend any products.

Simply explain what you understood from the user's request
and tell the user that suitable products have been found.
"""

        try:

            response = self.client.models.generate_content(
                model=LLM_MODEL,
                contents=prompt
            )

            return response.text.strip()

        except Exception as error:

            print(f"Gemini API Error: {error}")

            return (
                "I understood your request and searched the available "
                "products. Here are the most suitable recommendations."
            )
