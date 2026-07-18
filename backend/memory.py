# backend/memory.py
"""Conversational memory management for multi-turn shopping queries."""
from typing import Dict, List, Optional
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from pydantic import BaseModel, Field


class InMemoryChatMessageHistory(BaseChatMessageHistory, BaseModel):
    """
    In-memory chat message history with configurable window size.
    Stores messages per session_id for multi-user support.
    """
    messages: List[BaseMessage] = Field(default_factory=list)
    max_messages: int = Field(default=10)
    
    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add messages and enforce window size limit."""
        self.messages.extend(messages)
        # Keep only last N messages to prevent context overflow
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def clear(self) -> None:
        """Clear all messages."""
        self.messages = []
    
    def get_messages(self) -> List[BaseMessage]:
        """Return current message list."""
        return self.messages.copy()


# Global store: session_id -> chat history
_session_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str, max_messages: int = 10) -> InMemoryChatMessageHistory:
    """
    Retrieve or create chat history for a given session.
    
    Args:
        session_id: Unique identifier for the conversation session
        max_messages: Maximum number of messages to retain in memory
        
    Returns:
        InMemoryChatMessageHistory instance for the session
    """
    if session_id not in _session_store:
        _session_store[session_id] = InMemoryChatMessageHistory(max_messages=max_messages)
    return _session_store[session_id]


def clear_session_history(session_id: str) -> None:
    """Clear history for a specific session."""
    if session_id in _session_store:
        _session_store[session_id].clear()


def get_all_session_ids() -> List[str]:
    """Return all active session IDs (useful for debugging)."""
    return list(_session_store.keys())


def format_history_for_prompt(session_id: str) -> List[BaseMessage]:
    """
    Format chat history for injection into the prompt.
    Returns empty list if no history exists.
    """
    history = get_session_history(session_id)
    return history.get_messages()