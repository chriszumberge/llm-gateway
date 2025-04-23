import os
import httpx
from dotenv import load_dotenv
from gateway.schemas import ChatRequest, ChatResponse, EmbedRequest, EmbedResponse, ImageRequest

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_KEY      = os.getenv("AZURE_OPENAI_KEY")
AZURE_API_VER  = os.getenv("AZURE_OPENAI_API_VERSION")

if not (AZURE_ENDPOINT and AZURE_KEY and AZURE_API_VER):
    raise RuntimeError("Azure OpenAI config missing in .env")

BASE_URL = f"{AZURE_ENDPOINT}/openai"
HEADERS = {
    "api-key": AZURE_KEY,
    "Content-Type": "application/json",
}

def _deployment_path(deployment: str) -> str:
    return f"{BASE_URL}/deployments/{deployment}"

def handle_chat(req: ChatRequest) -> ChatResponse:
    # For Azure, req.model is actually the deployment name
    url = f"{_deployment_path(req.model)}/chat/completions?api-version={AZURE_API_VER}"
    body = {
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "temperature": req.temperature,
        "top_p": req.top_p,
    }
    if req.max_tokens is not None:
        body["max_tokens"] = req.max_tokens
    if req.functions:
        body["functions"] = [f.dict() for f in req.functions]

    r = httpx.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    data = r.json()
    choice = data["choices"][0]["message"]
    finish = data["choices"][0].get("finish_reason")
    usage = data.get("usage")

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
    url = f"{_deployment_path(req.model)}/chat/completions?api-version={AZURE_API_VER}"
    body = {
        "messages": [m.dict(exclude_none=True) for m in req.messages],
        "temperature": req.temperature,
        "top_p": req.top_p,
        "stream": True,
    }
    if req.max_tokens is not None:
        body["max_tokens"] = req.max_tokens
    if req.functions:
        body["functions"] = [f.dict() for f in req.functions]

    with httpx.stream("POST", url, headers=HEADERS, json=body) as resp:
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True):
            if line:
                yield f"{line}\n\n"

def handle_embed(req: EmbedRequest) -> EmbedResponse:
    url = f"{_deployment_path(req.model)}/embeddings?api-version={AZURE_API_VER}"
    body = {"input": req.input}
    r = httpx.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    data = r.json()
    vectors = [item["embedding"] for item in data["data"]]
    return EmbedResponse(embeddings=vectors, usage=data.get("usage"))

def handle_image(req: ImageRequest) -> bytes:
    url = f"{_deployment_path(req.model)}/images/generations?api-version={AZURE_API_VER}"
    body = {
        "prompt": req.prompt,
        "n": req.n,
        "size": req.size,
        "response_format": "b64_json",
    }
    if req.params:
        body.update(req.params)
    r = httpx.post(url, headers=HEADERS, json=body)
    r.raise_for_status()
    data = r.json()
    b64 = data["data"][0]["b64_json"]
    import base64
    return base64.b64decode(b64) 