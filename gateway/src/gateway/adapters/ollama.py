import httpx
from gateway.schemas import ChatRequest, ChatResponse, EmbedRequest, EmbedResponse, ImageRequest

BASE_URL = "http://localhost:11434/api"

def handle_chat(req: ChatRequest) -> ChatResponse:
    r = httpx.post(f"{BASE_URL}/chat", json={
        "model": req.model,
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "stream": False,
    })
    r.raise_for_status()
    data = r.json()
    msg = data["choices"][0]["message"]
    return ChatResponse(
        role=msg["role"],
        content=msg["content"],
        name=msg.get("name"),
        finish_reason=data["choices"][0].get("finish_reason"),
        usage=None,
    )

def stream_chat(req: ChatRequest):
    r = httpx.stream("POST", f"{BASE_URL}/chat", json={
        "model": req.model,
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "stream": True,
    })
    for line in r.iter_lines(decode_unicode=True):
        if line:
            yield f"data: {line}\n\n"

def handle_embed(req: EmbedRequest) -> EmbedResponse:
    r = httpx.post(f"{BASE_URL}/embed", json={
        "model": req.model,
        "input": req.input,
    })
    r.raise_for_status()
    data = r.json()
    return EmbedResponse(embeddings=data["embeddings"], usage=None)

def handle_image(req: ImageRequest) -> bytes:
    # Ollama doesn't support image gen—raise
    raise NotImplementedError("Ollama does not support image generation") 