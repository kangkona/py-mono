"""Data models for web UI."""

from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """A chat message."""

    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: str | None = None


class ChatRequest(BaseModel):
    """Chat request from client."""

    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    """Chat response to client."""

    content: str
    role: Literal["assistant"] = "assistant"
    conversation_id: str | None = None


class StreamChunk(BaseModel):
    """Streaming response chunk."""

    type: Literal["start", "token", "done", "error"]
    content: str | None = None
    error: str | None = None
