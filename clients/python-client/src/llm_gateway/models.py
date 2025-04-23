from typing import List, Optional, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    name: Optional[str] = None
    content: str

class ChatResponse(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    finish_reason: Optional[str] = None
    usage: Optional[Any] = None

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    usage: Optional[Any] = None