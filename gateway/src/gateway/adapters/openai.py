import os
import httpx
import base64
from dotenv import load_dotenv
from gateway.schemas import ChatRequest, ChatResponse, EmbedRequest, EmbedResponse, ImageRequest

# Load .env into environment
load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in environment")
BASE_URL = "https://api.openai.com/v1"
HEADERS = {
    "Authorization": f"Bearer {OPENAI_KEY}",
    "Content-Type": "application/json",
}

def handle_chat(req: ChatRequest) -> ChatResponse:
    # Build OpenAI payload
    body: dict = {
        "model": req.model,
        "messages": [
            {k: v for k, v in m.dict(exclude_none=True).items() if k in ("role", "name", "content")}
            for m in req.messages
        ],
        "temperature": req.temperature,
        "top_p": req.top_p,
    }
    if req.max_tokens is not None:
        body["max_tokens"] = req.max_tokens
    if req.functions:
        # Pydantic .dict() on FunctionDef gives name, description, parameters
        body["functions"] = [f.dict() for f in req.functions]

    # Call OpenAI
    resp = httpx.post(f"{BASE_URL}/chat/completions", headers=HEADERS, json=body)
    resp.raise_for_status()
    data = resp.json()

    choice = data["choices"][0]["message"]
    finish = data["choices"][0].get("finish_reason")
    usage = data.get("usage")

    # If function_call, pull out name & arguments
    func = choice.get("function_call")
    name = func["name"] if func else None
    content = func["arguments"] if func else choice.get("content", "")

    return ChatResponse(
        role=choice["role"],
        content=content,
        name=name,
        finish_reason=finish,
        usage=usage,
    )

def stream_chat(req: ChatRequest):
    body = {
        "model": req.model,
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "temperature": req.temperature,
        "top_p": req.top_p,
        "stream": True,
    }
    if req.max_tokens is not None:
        body["max_tokens"] = req.max_tokens
    if req.functions:
        body["functions"] = [f.dict() for f in req.functions]

    # open a streaming request
    with httpx.stream("POST", f"{BASE_URL}/chat/completions", headers=HEADERS, json=body) as resp:
        resp.raise_for_status()
        # resp.iter_lines(decode_unicode=True) yields each line in the SSE.
        for line in resp.iter_lines(decode_unicode=True):
            if not line:
                continue
            # line is like "data: {...}" or "data: [DONE]"
            yield f"{line}\n\n"

def handle_embed(req: EmbedRequest) -> EmbedResponse:
    body = {"model": req.model, "input": req.input}
    resp = httpx.post(f"{BASE_URL}/embeddings", headers=HEADERS, json=body)
    resp.raise_for_status()
    data = resp.json()
    vectors = [item["embedding"] for item in data["data"]]
    usage = data.get("usage")
    return EmbedResponse(embeddings=vectors, usage=usage)

def handle_image(req: ImageRequest) -> bytes:
    if req.n != 1:
        raise ValueError("Only n=1 is supported currently")
    body: dict = {
        "prompt": req.prompt,
        "n": 1,
        "size": req.size,
        # we ask for base64 so we can decode on the gateway
        "response_format": "b64_json",
    }
    # include any extra provider params untouched
    if req.params:
        body.update(req.params)

    resp = httpx.post(f"{BASE_URL}/images/generations", headers=HEADERS, json=body)
    resp.raise_for_status()
    data = resp.json()
    b64 = data["data"][0]["b64_json"]
    return base64.b64decode(b64)