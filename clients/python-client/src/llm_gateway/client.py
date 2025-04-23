import httpx
from typing import List, Optional
from .models import ChatResponse, EmbedResponse

class GatewayClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        self._base = base_url.rstrip("/")
        self._headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
        self._client = httpx.Client(headers=self._headers, timeout=timeout)

    def chat(self,
             model: str,
             messages: List[dict],
             provider: str = "openai",
             functions: Optional[List[dict]] = None,
             temperature: float = 1.0,
             max_tokens: Optional[int] = None,
             top_p: float = 1.0) -> ChatResponse:
        payload = {
            "provider": provider,
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if functions:
            payload["functions"] = functions

        r = self._client.post(f"{self._base}/chat", json=payload)
        r.raise_for_status()
        return ChatResponse.model_validate(r.json())

    def stream_chat(self, *args, **kwargs):
        payload = {"stream": True, **kwargs}
        r = self._client.post(f"{self._base}/chat/stream", json=payload, stream=True)
        r.raise_for_status()
        for line in r.iter_lines():
            yield line.decode().strip()

    def embed(self, model: str, input: List[str], provider: str = "openai") -> EmbedResponse:
        payload = {"provider": provider, "model": model, "input": input}
        r = self._client.post(f"{self._base}/embed", json=payload)
        r.raise_for_status()
        return EmbedResponse.model_validate(r.json())

    def generate_image(self,
                       model: str,
                       prompt: str,
                       size: str = "512x512",
                       n: int = 1,
                       params: dict = None,
                       provider: str = "openai") -> bytes:
        payload = {
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n,
        }
        if params:
            payload["params"] = params
        r = self._client.post(f"{self._base}/image", json=payload)
        r.raise_for_status()
        return r.content