
# Create rag_pipeline.py

from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage

# Simulated LLM for demo purposes (no API key required)
class SimulatedLLM:
    """A simulated LLM that generates responses based on product context."""
    
    def invoke(self, messages):
        # Extract the last human message and context
        human_msg = None
        context = ""
        for msg in messages:
            if hasattr(msg, 'type') and msg.type == 'human':
                human_msg = msg.content
            elif hasattr(msg, 'type') and msg.type == 'system' and 'Catalogue context' in msg.content:
                context = msg.content
        
        if not human_msg:
            human_msg = "Find me some products"
        
        # Generate a response based on the products in context
        products_in_context = self._extract_products(context)
        
        if not products_in_context:
            response_text = "I couldn't find any products matching your request. Try broadening your search or increasing your budget."
        else:
            response_text = self._generate_recommendation(human_msg, products_in_context)
        
        class Response:
            def __init__(self, content):
                self.content = content
        
        return Response(response_text)
    
    def _extract_products(self, context: str) -> List[Dict]:
        """Extract product info from context text."""
        products = []
        # Split by "Product X:" pattern
        parts = re.split(r'Product \d+:', context)
        for part in parts[1:]:  # Skip first empty part
            product = {}
            # Extract name
            name_match = re.search(r'^(.+?) by', part)
            if name_match:
                product['name'] = name_match.group(1).strip()
            
            # Extract brand
            brand_match = re.search(r'by ([^.]+)', part)
            if brand_match:
                product['brand'] = brand_match.group(1).strip()
            
            # Extract price
            price_match = re.search(r'discounted price: ([^;]+)', part)
            if price_match:
                product['price'] = price_match.group(1).strip()
            
            # Extract rating
            rating_match = re.search(r'Rating: ([^/]+)', part)
            if rating_match:
                product['rating'] = rating_match.group(1).strip()
            
            # Extract discount
            discount_match = re.search(r'discount: ([^%]+)%', part)
            if discount_match:
                product['discount'] = discount_match.group(1).strip()
            
            # Extract stock
            stock_match = re.search(r'Stock: ([^.]+)', part)
            if stock_match:
                product['stock'] = stock_match.group(1).strip()
            
            if product:
                products.append(product)
        
        return products
    
    def _generate_recommendation(self, query: str, products: List[Dict]) -> str:
        """Generate a natural recommendation response."""
        query_lower = query.lower()
        
        # Determine tone based on query
        if 'budget' in query_lower or 'under' in query_lower or 'cheap' in query_lower:
            intro = "Here are some great budget-friendly options for you:"
        elif 'best' in query_lower or 'top' in query_lower or 'highest' in query_lower:
            intro = "Here are the top-rated options I found:"
        elif 'brand' in query_lower:
            intro = "Here are products from your preferred brand:"
        else:
            intro = "Based on your request, here are my recommendations:"
        
        lines = [intro, ""]
        
        for i, prod in enumerate(products[:3], 1):
            name = prod.get('name', 'Unknown Product')
            brand = prod.get('brand', '')
            price = prod.get('price', 'N/A')
            rating = prod.get('rating', 'N/A')
            discount = prod.get('discount', '0')
            stock = prod.get('stock', 'Unknown')
            
            lines.append(f"**{i}. {name}** | {price}")
            lines.append(f"   - Brand: {brand}")
            lines.append(f"   - Rating: {rating}/5 ⭐")
            lines.append(f"   - Discount: {discount}% off")
            lines.append(f"   - Stock: {stock}")
            
            # Add a personalized reason
            if float(rating) >= 4.5:
                lines.append(f"   - Why: Highly rated by customers with excellent reviews.")
            elif int(discount) >= 50:
                lines.append(f"   - Why: Massive {discount}% discount makes this a steal!")
            elif 'In Stock' in stock:
                lines.append(f"   - Why: Available for immediate purchase with good ratings.")
            else:
                lines.append(f"   - Why: Great value proposition from a trusted brand.")
            
            lines.append("")
        
        lines.append("Would you like me to compare these options, filter by a specific brand, or show alternatives?")
        
        return "\n".join(lines)


def initialize_llm():
    """Initialize the LLM - uses simulated version for demo."""
    return SimulatedLLM()


# Import from config (using relative imports for flexibility)
try:
    from backend.config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE, MAX_HISTORY_MESSAGES, PRODUCT_CSV_PATH
except ImportError:
    from config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE, MAX_HISTORY_MESSAGES, PRODUCT_CSV_PATH

try:
    from backend.memory import format_history_for_prompt, get_session_history
except ImportError:
    from memory import format_history_for_prompt, get_session_history

try:
    from backend.models import AssistantResponse, ProductSource
except ImportError:
    from models import AssistantResponse, ProductSource

try:
    from backend.prompts import get_chat_prompt
except ImportError:
    from prompts import get_chat_prompt

REQUIRED_COLUMNS = {"product_id", "product_name", "brand", "category", "subcategory", "price", "currency", "discount_percent", "discounted_price", "rating", "reviews_count", "popularity_score", "stock_status", "date_added", "description"}
STOP_WORDS = {"a", "an", "and", "are", "best", "for", "give", "i", "in", "is", "me", "of", "product", "recommend", "show", "the", "to", "with"}


def _number(value: str, field: str, product_id: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid {field} for product {product_id}: {value!r}") from exc


def _product_text(product: Dict[str, Any]) -> str:
    return (f"{product['product_name']} by {product['brand']}. Category: {product['category']}; "
            f"subcategory: {product['subcategory']}. Price: {product['currency']} {product['price']}; "
            f"discounted price: {product['currency']} {product['discounted_price']}; discount: {product['discount_percent']}%. "
            f"Rating: {product['rating']}/5 from {product['reviews_count']} reviews. Popularity score: {product['popularity_score']}. "
            f"Stock: {product['stock_status']}. Description: {product['description']}")


@lru_cache(maxsize=1)
def load_catalogue() -> List[Document]:
    """Load, validate, and turn the actual CSV rows into searchable documents."""
    csv_path = Path(PRODUCT_CSV_PATH).expanduser()
    if not csv_path.is_file():
        raise FileNotFoundError(f"Product CSV not found at {csv_path}. Set PRODUCT_CSV_PATH in .env.")
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Product CSV is missing required columns: {', '.join(sorted(missing))}")
        documents = []
        for row in reader:
            product_id = row["product_id"].strip()
            if not product_id or not row["product_name"].strip():
                continue
            metadata = {**row, "price_value": _number(row["price"], "price", product_id), "discounted_price_value": _number(row["discounted_price"], "discounted_price", product_id), "rating_value": _number(row["rating"], "rating", product_id), "popularity_score_value": _number(row["popularity_score"], "popularity_score", product_id), "source": str(csv_path)}
            documents.append(Document(page_content=_product_text(metadata), metadata=metadata))
    if not documents:
        raise ValueError("Product CSV contains no valid products.")
    return documents


def _tokens(query: str) -> List[str]:
    return [token for token in re.findall(r"[a-z0-9]+", query.lower()) if len(token) > 1 and token not in STOP_WORDS]


def _budget_limit(query: str) -> Optional[float]:
    match = re.search(r"(?:under|below|less than|upto|up to|within)\s*(?:₹|rs\.?|inr)?\s*([\d,]+)", query.lower())
    return float(match.group(1).replace(",", "")) if match else None


def retrieve_products(query: str, k: int = 5) -> List[Document]:
    """Rank real CSV products; filter by discounted price and requested availability."""
    tokens, budget, query_lower = _tokens(query), _budget_limit(query), query.lower()
    wants_available = any(term in query_lower for term in ("in stock", "available", "buy now"))
    ranked = []
    for doc in load_catalogue():
        data = doc.metadata
        if budget is not None and data["discounted_price_value"] > budget:
            continue
        if wants_available and data["stock_status"].lower() == "out of stock":
            continue
        searchable = " ".join(str(data[field]).lower() for field in ("product_name", "brand", "category", "subcategory", "description"))
        matches = sum(token in searchable for token in tokens)
        if tokens and not matches:
            continue
        score = matches * 100 + data["rating_value"] * 2 + data["popularity_score_value"] / 100000
        ranked.append((score, doc))
    return [doc for _, doc in sorted(ranked, key=lambda item: item[0], reverse=True)[:k]]


def _response_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\\n".join(item.get("text", "") if isinstance(item, dict) else getattr(item, "text", str(item)) for item in content)
    return str(content)


def _to_source(doc: Document) -> ProductSource:
    data = doc.metadata
    facts = f"{data['brand']} | {data['rating']}/5 ({data['reviews_count']} reviews) | {data['discount_percent']}% off | {data['stock_status']}"
    return ProductSource(name=data["product_name"], price=f"{data['currency']} {data['discounted_price']}", category=data["category"], specs=facts, source=data["source"], product_id=data["product_id"], brand=data["brand"], subcategory=data["subcategory"], rating=data["rating_value"], stock_status=data["stock_status"])


def _follow_ups(query: str, sources: List[ProductSource]) -> List[str]:
    if not sources:
        return ["Show products in another category", "Increase my budget", "Show products that are in stock"]
    if _budget_limit(query) is not None:
        return ["Show the highest-rated option", "Compare these products", "Show options with a larger discount"]
    return ["Compare the top two options", "Which option has the most reviews?", "Show only products that are in stock"]


def generate_assistant_response(user_query: str, session_id: str = "default_session", chat_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    if not user_query or not user_query.strip():
        raise ValueError("user_query must not be empty.")
    history = get_session_history(session_id, max_messages=MAX_HISTORY_MESSAGES)
    if chat_history is not None:
        history.clear()
        history.add_messages([HumanMessage(content=item["content"]) if item.get("role") == "user" else AIMessage(content=item["content"]) for item in chat_history if item.get("role") in {"user", "assistant"} and item.get("content")])
    documents = retrieve_products(user_query)
    if documents:
        context = "\\n\\n".join(f"Product {index}: {doc.page_content}" for index, doc in enumerate(documents, 1))
        response = initialize_llm().invoke(get_chat_prompt().format_messages(input=user_query, context=context, chat_history=format_history_for_prompt(session_id)))
        answer = _response_text(response.content)
    else:
        answer = "No products in the catalogue match that request. Try a higher budget or another category."
    history.add_messages([HumanMessage(content=user_query), AIMessage(content=answer)])
    sources = [_to_source(doc) for doc in documents]
    return AssistantResponse(answer=answer, sources=sources, session_id=session_id, follow_up_suggestions=_follow_ups(user_query, sources)).model_dump()


def get_session_summary(session_id: str) -> Dict[str, Any]:
    messages = get_session_history(session_id).get_messages()
    return {"session_id": session_id, "total_messages": len(messages), "user_messages": sum(isinstance(message, HumanMessage) for message in messages), "assistant_messages": sum(isinstance(message, AIMessage) for message in messages), "message_preview": [{"role": "user" if isinstance(message, HumanMessage) else "assistant", "content": str(message.content)[:100]} for message in messages[-4:]]}


def reset_conversation(session_id: str) -> bool:
    try:
        from backend.memory import clear_session_history
    except ImportError:
        from memory import clear_session_history
    clear_session_history(session_id)
    return True





