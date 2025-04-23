import os
import httpx
from dotenv import load_dotenv
from gateway.schemas import ChatRequest, ChatResponse

load_dotenv()

CLAUDE_KEY     = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_VERSION = os.getenv("ANTHROPIC_API_VERSION")

if not (CLAUDE_KEY and CLAUDE_VERSION):
    raise RuntimeError("Anthropic config missing")

BASE_URL = "https://api.anthropic.com/v1"

HEADERS = {
    "x-api-key": CLAUDE_KEY,
    "anthropic-version": CLAUDE_VERSION,
    "Content-Type": "application/json",
}

def handle_chat(req: ChatRequest) -> ChatResponse:
    url = f"{BASE_URL}/messages"
    # Claude v2+ uses messages array
    body = {
        "model": req.model,
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "max_tokens": req.max_tokens or 1000,
        "temperature": req.temperature,
        "top_p": req.top_p,
    }
    # Anthropic uses `tools` instead of `functions`
    if req.functions:
        tools = []
        for f in req.functions:
            tools.append({
                "name": f.name,
                "description": f.description,
                "input_schema": f.parameters,
            })
        body["tools"] = tools

    r = httpx.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    data = r.json()

    # Claude returns content in the content array
    content = data["content"][0]["text"]
    # Detect tool use in stop_reason
    finish = data.get("stop_reason")
    # Anthropic doesn't give usage currently in v2
    return ChatResponse(
        role="assistant",
        content=content,
        name=None,
        finish_reason=finish,
        usage=None,
    )

def stream_chat(req: ChatRequest):
    url = f"{BASE_URL}/messages"
    body = {
        "model": req.model,
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "stream": True,
        "max_tokens": req.max_tokens or 1000,
        "temperature": req.temperature,
        "top_p": req.top_p,
    }
    if req.functions:
        body["tools"] = [
            {"name": f.name, "description": f.description, "input_schema": f.parameters}
            for f in req.functions
        ]

    with httpx.stream("POST", url, headers=HEADERS, json=body) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if line.startswith("data: "):
                yield f"{line}\n\n"

# Embeddings and image generation not supported by Claude
def handle_embed(req, *args, **kwargs):
    raise NotImplementedError("Claude does not support embeddings")

def handle_image(req, *args, **kwargs):
    raise NotImplementedError("Claude does not support image generation") 