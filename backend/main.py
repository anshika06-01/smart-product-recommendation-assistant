"""FastAPI service for the CSV-backed ShopWise assistant."""
from typing import List, Literal, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from BACKEND.rag_pipeline import (
    generate_assistant_response,
    get_session_summary,
    reset_conversation,
)

app = FastAPI(
    title="ShopWise Recommendation API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class RecommendationRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    session_id: str = Field(default="default_session", min_length=1)
    chat_history: Optional[List[ChatMessage]] = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/recommendations")
def recommend(request: RecommendationRequest):
    try:
        history = (
            [message.model_dump() for message in request.chat_history]
            if request.chat_history
            else None
        )
        return generate_assistant_response(
            request.query,
            request.session_id,
            history,
        )
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unable to generate recommendation. Check API configuration.",
        ) from exc


@app.get("/api/sessions/{session_id}")
def session_summary(session_id: str):
    return get_session_summary(session_id)


@app.delete("/api/sessions/{session_id}")
def clear_session(session_id: str):
    reset_conversation(session_id)
    return {"session_id": session_id, "cleared": True}