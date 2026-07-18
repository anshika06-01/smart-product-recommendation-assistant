# backend/models.py
"""Pydantic models for structured RAG pipeline outputs."""
from typing import List, Optional
from pydantic import BaseModel, Field


class ProductSource(BaseModel):
    """Represents a source product document from the vector store."""
    name: str = Field(description="Product name")
    price: str = Field(description="Product price (with currency)")
    category: str = Field(description="Product category")
    specs: str = Field(description="Dataset facts: brand, rating, reviews, discount, and stock")
    source: str = Field(description="Source document identifier")
    score: Optional[float] = Field(default=None, description="Relevance score")
    product_id: Optional[str] = Field(default=None, description="Catalogue product ID")
    brand: Optional[str] = Field(default=None, description="Product brand")
    subcategory: Optional[str] = Field(default=None, description="Product subcategory")
    rating: Optional[float] = Field(default=None, description="Product rating")
    stock_status: Optional[str] = Field(default=None, description="Current catalogue stock status")


class AssistantResponse(BaseModel):
    """Structured output from the RAG pipeline."""
    answer: str = Field(description="The conversational answer text")
    sources: List[ProductSource] = Field(default_factory=list, description="Referenced product sources")
    session_id: str = Field(description="Session identifier for continuity")
    follow_up_suggestions: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up questions"
    )


class FilterParams(BaseModel):
    """Structured filter parameters extracted from user query."""
    max_price: Optional[float] = Field(default=None, description="Maximum budget in INR")
    min_price: Optional[float] = Field(default=None, description="Minimum budget in INR")
    category: Optional[str] = Field(default=None, description="Product category")
    brand: Optional[str] = Field(default=None, description="Preferred brand")
    features: List[str] = Field(default_factory=list, description="Required features")
