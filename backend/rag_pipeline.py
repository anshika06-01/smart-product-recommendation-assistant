# backend/rag_pipeline.py

from typing import List, Dict, Any, Optional
import os
from urllib import response

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

# Import your modules
from BACKEND.config import GOOGLE_API_KEY, LLM_MODEL, LLM_TEMPERATURE, MAX_HISTORY_MESSAGES
from BACKEND.prompts import get_chat_prompt
from BACKEND.memory import get_session_history, format_history_for_prompt
from BACKEND.models import AssistantResponse, ProductSource


MOCK_PRODUCTS = [
    {
        "name": "Sony WH-CH720N Wireless Headphones",
        "price": "₹7,990",
        "category": "Headphones",
        "specs": "Noise Cancellation, 35h Battery, Bluetooth 5.0, 192g",
        "description": "Lightweight wireless headphones with digital noise cancellation."
    },
    {
        "name": "boAt Rockerz 450 Bluetooth Headphones",
        "price": "₹1,499",
        "category": "Headphones",
        "specs": "15h Battery, Bluetooth 5.0, 40mm Drivers, IPX5",
        "description": "Budget-friendly wireless headphones with deep bass."
    },
    {
        "name": "JBL Tune 760NC",
        "price": "₹5,999",
        "category": "Headphones",
        "specs": "Active NC, 35h Battery, Multi-point, 220g",
        "description": "Over-ear wireless headphones with adaptive noise cancelling."
    },
    {
        "name": "realme Buds T300 TWS",
        "price": "₹2,299",
        "category": "Earbuds",
        "specs": "30h Total Battery, IP55, 12.4mm Driver, Bluetooth 5.3",
        "description": "True wireless earbuds with long battery life and water resistance."
    },
    {
        "name": "Noise Buds VS104",
        "price": "₹999",
        "category": "Earbuds",
        "specs": "30h Battery, IPX5, Quad Mic ENC, 13mm Driver",
        "description": "Ultra-budget TWS earbuds with environmental noise cancellation."
    }
]


class MockVectorStore:
    """Mock vector store for Day 2 testing."""
    
    def __init__(self, products: List[Dict]):
        self.products = products
        self.documents = [
            Document(
                page_content=f"{p['name']}. {p['description']}. Price: {p['price']}. Specs: {p['specs']}.",
                metadata={
                    "name": p["name"],
                    "price": p["price"],
                    "category": p["category"],
                    "specs": p["specs"],
                    "source": "mock_db"
                }
            )
            for p in products
        ]
    
    def similarity_search(self, query: str, k: int = 5, filter: Optional[Dict] = None) -> List[Document]:
        """Mock similarity search - returns all docs for now."""
        # Simple keyword matching mock
        query_lower = query.lower()
        results = []
        for doc in self.documents:
            score = sum(1 for word in query_lower.split() if word in doc.page_content.lower())
            if score > 0 or not query_lower:
                results.append(doc)
        return results[:k] if results else self.documents[:k]
    
    def as_retriever(self, **kwargs):
        """Return a mock retriever."""
        from langchain_core.retrievers import BaseRetriever
        from langchain_core.callbacks import CallbackManagerForRetrieverRun
        
        class MockRetriever(BaseRetriever):
            def _get_relevant_documents(self, query: str, *, run_manager: CallbackManagerForRetrieverRun = None) -> List[Document]:
                return self.similarity_search(query, k=kwargs.get('search_kwargs', {}).get('k', 5))
        
        retriever = MockRetriever()
        retriever.similarity_search = self.similarity_search
        return retriever


class MockFilterWrapper:
    """Mock filter wrapper for Day 2 testing."""
    
    def __init__(self, vector_store, llm):
        self.vector_store = vector_store
        self.llm = llm
    
    def invoke(self, query: str) -> List[Document]:
        """Mock retrieval with simple filtering."""
        docs = self.vector_store.similarity_search(query, k=10)
        # Simple price filter mock
        if "under" in query.lower() or "below" in query.lower():
            # Extract number (mock)
            import re
            numbers = re.findall(r'[\d,]+', query)
            if numbers:
                max_price = int(numbers[0].replace(',', ''))
                filtered = []
                for doc in docs:
                    price_str = doc.metadata.get("price", "₹0")
                    price_num = int(price_str.replace("₹", "").replace(",", ""))
                    if price_num <= max_price:
                        filtered.append(doc)
                return filtered if filtered else docs
        return docs


# LLM INITIALIZATION


def initialize_llm() -> ChatGoogleGenerativeAI:
    """
    Initialize the Google Gemini LLM via LangChain.
    
    Returns:
        Configured ChatGoogleGenerativeAI instance
    """
    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        google_api_key=GOOGLE_API_KEY,
        max_output_tokens=2048,
    )

# MASTER RESPONSE FUNCTION 


def generate_assistant_response(
    user_query: str,
    session_id: str = "default_session",
    chat_history: Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Master execution hook for the shopping assistant.
    
    This is the PRIMARY function that Gauri's Streamlit frontend invokes.
    It processes the full RAG pipeline and returns structured output.
    
    Args:
        user_query: Raw user query string
        session_id: Unique session identifier for conversation continuity
        chat_history: Optional pre-existing chat history (for frontend sync)
        
    Returns:
        Dictionary with 'answer', 'sources', 'session_id', 'follow_up_suggestions'
    """
    # Step 1: Initialize LLM
    llm = initialize_llm()
    
    # Step 2: Get or create session history
    session_history = get_session_history(session_id, max_messages=MAX_HISTORY_MESSAGES)
    
    # If frontend provides history, sync it
    if chat_history:
        session_history.clear()
        for msg in chat_history:
            if msg.get("role") == "user":
                session_history.add_messages([HumanMessage(content=msg["content"])])
            elif msg.get("role") == "assistant":
                session_history.add_messages([AIMessage(content=msg["content"])])
    
    # Step 3: Retrieve context (MOCK for Day 2)
    mock_db = MockVectorStore(MOCK_PRODUCTS)
    smart_retriever = MockFilterWrapper(mock_db, llm)
    retrieved_docs = smart_retriever.invoke(user_query)
    
    # Format context for prompt
    context_text = "\n\n".join([
        f"Product {i+1}:\nName: {doc.metadata.get('name', 'N/A')}\n"
        f"Price: {doc.metadata.get('price', 'N/A')}\n"
        f"Specs: {doc.metadata.get('specs', 'N/A')}\n"
        f"Description: {doc.page_content}"
        for i, doc in enumerate(retrieved_docs)
    ])
    
    # Step 4: Build prompt with history
    prompt = get_chat_prompt()
    history_messages = format_history_for_prompt(session_id)
    
    # Step 5: Create RAG chain
    
    
    # For mock mode, we manually construct the response since we don't have real retriever
    from langchain_core.runnables import RunnablePassthrough
    
    # Manual invocation 
    chain_input = {
        "input": user_query,
        "context": context_text,
        "chat_history": history_messages
    }



    # Generate response
        # Generate response
    response = llm.invoke(
        prompt.format_messages(
            input=user_query,
            context=context_text,
            chat_history=history_messages
        )
    )

    print("Type:", type(response.content))
    print("Content:", response.content)

    # Convert Gemini response into plain text
    if isinstance(response.content, str):
        answer_text = response.content

    elif isinstance(response.content, list):
        text_parts = []

        for item in response.content:

            if isinstance(item, dict):
                if item.get("type") == "text":
                    text_parts.append(item.get("text", ""))

            elif hasattr(item, "text"):
                text_parts.append(item.text)

            else:
                text_parts.append(str(item))

        answer_text = "\n".join(text_parts)

    else:
        answer_text = str(response.content)

    print("Extracted Answer:")
    print(answer_text)
    
   
     

    
    # Step 6: Update session history
    session_history.add_messages([
        HumanMessage(content=user_query),
        AIMessage(content=answer_text)
    ])
    
    # Step 7: Build structured sources
    sources = [
        ProductSource(
            name=doc.metadata.get("name", "Unknown"),
            price=doc.metadata.get("price", "N/A"),
            category=doc.metadata.get("category", "N/A"),
            specs=doc.metadata.get("specs", "N/A"),
            source=doc.metadata.get("source", "unknown"),
            score=None
        )
        for doc in retrieved_docs
    ]
    
    # Step 8: Generate follow-up suggestions
    follow_ups = _generate_follow_up_suggestions(user_query, answer_text, sources)
    
    # Step 9: Return structured payload
    result = AssistantResponse(
        answer=answer_text,
        sources=sources,
        session_id=session_id,
        follow_up_suggestions=follow_ups
    )
    
    return result.model_dump()


def _generate_follow_up_suggestions(query: str, answer: str, sources: List[ProductSource]) -> List[str]:
    """
    Generate contextual follow-up question suggestions.
    """
    suggestions = []
    
    # Budget-related follow-ups
    if any(word in query.lower() for word in ["under", "below", "cheap", "budget"]):
        suggestions.append("What if I increase my budget slightly?")
        suggestions.append("Are there any discount offers on these?")
    
    # Feature-related follow-ups
    if "waterproof" in query.lower() or "ipx" in query.lower():
        suggestions.append("What's the difference between IPX5 and IPX7?")
        suggestions.append("Can I swim with these?")
    elif "battery" in query.lower():
        suggestions.append("How long does the battery last with ANC on?")
        suggestions.append("Does it support fast charging?")
    
    # General follow-ups
    if not suggestions:
        suggestions.append("Compare the top 2 options for me")
        suggestions.append("What are the main differences in specs?")
        suggestions.append("Which one has the best reviews?")
    
    return suggestions[:3]

# UTILITY FUNCTIONS


def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Get conversation summary for a session (useful for debugging).
    """
    history = get_session_history(session_id)
    messages = history.get_messages()
    
    return {
        "session_id": session_id,
        "total_messages": len(messages),
        "user_messages": sum(1 for m in messages if isinstance(m, HumanMessage)),
        "assistant_messages": sum(1 for m in messages if isinstance(m, AIMessage)),
        "message_preview": [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant", "content": m.content[:100]}
            for m in messages[-4:]
        ]
    }


def reset_conversation(session_id: str) -> bool:
    """
    Clear conversation history for a session.
    """
    from BACKEND.memory import clear_session_history
    clear_session_history(session_id)
    return True