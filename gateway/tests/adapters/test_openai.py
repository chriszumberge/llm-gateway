import httpx
import base64
import pytest
from gateway.adapters import openai as adapter
from gateway.schemas import ChatRequest, Message, EmbedRequest, ImageRequest

class DummyResponse:
    def __init__(self, json_data, text_data=None):
        self._json = json_data
        self.text = text_data or ""
    def raise_for_status(self): pass
    def json(self): return self._json

def test_handle_chat(monkeypatch):
    fake = {
        "choices": [{"message": {"role": "assistant", "content": "hi"}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}
    }
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = ChatRequest(provider="openai", model="m", messages=[Message(role="user", content="Hello")])
    resp = adapter.handle_chat(req)
    assert resp.content == "hi"
    assert resp.finish_reason == "stop"
    assert resp.usage["total_tokens"] == 2

def test_stream_chat(monkeypatch):
    def fake_stream(*args, **kwargs):
        class CM:
            def __enter__(self): return self
            def __exit__(self, *a): pass
            def iter_lines(self, decode_unicode):
                return iter(["data: hello", "data: [DONE]"])
            def raise_for_status(self): pass
        return CM()
    monkeypatch.setattr(httpx, "stream", fake_stream)
    req = ChatRequest(provider="openai", model="m", messages=[Message(role="user", content="Hello")])
    chunks = list(adapter.stream_chat(req))
    assert "hello" in chunks[0]

def test_handle_embed(monkeypatch):
    fake = {"data": [{"embedding":[0.1,0.2]}], "usage": {"total_tokens":3}}
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = EmbedRequest(provider="openai", model="m", input=["a"])
    resp = adapter.handle_embed(req)
    assert resp.embeddings == [[0.1,0.2]]
    assert resp.usage["total_tokens"] == 3

def test_handle_image(monkeypatch):
    b64 = base64.b64encode(b"imgdata").decode()
    fake = {"data": [{"b64_json": b64}]}
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = ImageRequest(provider="openai", model="m", prompt="p", size="512x512", n=1)
    data = adapter.handle_image(req)
    assert data == b"imgdata" 