from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str  # "system" | "user" | "assistant" | "function" | "tool"
    name: Optional[str] = None
    content: str

class FunctionDef(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema object

class ChatRequest(BaseModel):
    provider: str
    model: str
    messages: List[Message]
    functions: Optional[List[FunctionDef]] = None
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    top_p: Optional[float] = 1.0
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    role: str
    content: str
    name: Optional[str] = None
    finish_reason: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

class EmbedRequest(BaseModel):
    provider: str
    model: str
    input: List[str]

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    usage: Optional[Dict[str, Any]] = None

class ImageRequest(BaseModel):
    provider: str
    model: str
    prompt: str
    size: Optional[str] = "512x512"
    n: Optional[int] = 1
    params: Optional[Dict[str, Any]] = None 