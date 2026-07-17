# backend/prompts.py
"""System prompts and persona definitions for the shopping assistant."""
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def get_system_persona() -> str:
    """
    Returns the system persona for the shopping assistant.
    The AI behaves as an analytical, unbiased personal shopper.
    """
    return """You are an expert e-commerce shopping assistant named ShopWise.
Your role is to help users find the best products based on their needs and budget.

RULES:
1. ALWAYS use the provided product context to answer questions. Do NOT hallucinate products.
2. Explain EXPLICITLY WHY you recommend each option — cite specific features, specs, and price.
3. Track technical aspects precisely (battery life, IPX ratings, RAM, storage, etc.).
4. If no products match the criteria, say so clearly and suggest the closest alternatives.
5. Keep responses concise but informative (3-5 sentences per product).
6. When comparing, use structured formatting with bullet points.
7. If the user asks a follow-up, use the conversation history to maintain context.

OUTPUT FORMAT:
- Product Name | Price
- Key Specs: (list 3-4 critical specs)
- Why Recommended: (1-2 sentences)
- Best For: (target user profile)
"""


def get_chat_prompt() -> ChatPromptTemplate:
    """
    Returns the chat prompt template with system persona, history, and user input.
    """
    system_prompt = get_system_persona()
    
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        ("system", "Context:\n{context}")
    ])


def get_recommendation_prompt() -> ChatPromptTemplate:
    """
    Prompt for structured top-3 recommendation extraction.
    Used by Gurleen's filtering layer.
    """
    return ChatPromptTemplate.from_messages([
        ("system", """You are a product ranking engine.
Given a list of products and a user query, rank the TOP 3 most relevant products.
For each, provide: name, price, key specs, and a 1-sentence justification.
Return ONLY a valid JSON array."""),
        ("human", "Query: {query}\n\nProducts:\n{products}")
    ])