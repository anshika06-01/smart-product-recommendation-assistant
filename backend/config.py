# backend/config.py
"""Central configuration for API keys and environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

# Google Gemini API Key (Primary LLM)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")

# Model Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash-latest")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))

# Vector DB Configuration 
VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/embedding-001")

# Set PRODUCT_CSV_PATH in .env to the actual ecommerce catalogue location.
PRODUCT_CSV_PATH = os.getenv(
    "PRODUCT_CSV_PATH",
    os.path.join(os.path.dirname(__file__), "ecommerce_products_killer.csv"),
)

# Session Configuration
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "10"))
