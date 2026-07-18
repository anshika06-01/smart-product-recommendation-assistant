"""Print Google GenAI models available to the API key in .env."""
import os
import sys

from dotenv import load_dotenv
from google import genai


def main() -> int:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "replace_with_your_google_ai_api_key":
        print("GOOGLE_API_KEY is missing. Copy .env.example to .env and add a valid key.", file=sys.stderr)
        return 1

    try:
        client = genai.Client(api_key=api_key)
        models = sorted(client.models.list(), key=lambda model: model.name)
    except Exception as exc:
        print(f"Could not list Google models: {exc}", file=sys.stderr)
        return 1

    print("Available Google models:\n")
    for model in models:
        print(model.name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
