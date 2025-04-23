import httpx
import pytest
from gateway.adapters import ollama as adapter
from gateway.schemas import ChatRequest, Message, EmbedRequest, ImageRequest

class DummyResponse:
    def __init__(self, json_data, text_data=None):
        self._json = json_data
        self.text = text_data or ""
    def raise_for_status(self): pass
    def json(self): return self._json

def test_handle_chat(monkeypatch):
    fake = {
        "message": {"role": "assistant", "content": "hi"},
        "done": True,
        "total_duration": 100
    }
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = ChatRequest(provider="ollama", model="llama2", messages=[Message(role="user", content="Hello")])
    resp = adapter.handle_chat(req)
    assert resp.content == "hi"
    assert resp.finish_reason == "stop"
    assert resp.usage["total_tokens"] == 0  # Ollama doesn't provide token counts

def test_stream_chat(monkeypatch):
    def fake_stream(*args, **kwargs):
        class CM:
            def __enter__(self): return self
            def __exit__(self, *a): pass
            def iter_lines(self, decode_unicode):
                return iter(["data: {\"message\":{\"content\":\"hello\"}}", "data: {\"done\":true}"])
            def raise_for_status(self): pass
        return CM()
    monkeypatch.setattr(httpx, "stream", fake_stream)
    req = ChatRequest(provider="ollama", model="llama2", messages=[Message(role="user", content="Hello")])
    chunks = list(adapter.stream_chat(req))
    assert "hello" in chunks[0]

def test_handle_embed(monkeypatch):
    fake = {"embedding": [0.1, 0.2]}
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = EmbedRequest(provider="ollama", model="llama2", input=["a"])
    resp = adapter.handle_embed(req)
    assert resp.embeddings == [[0.1, 0.2]]
    assert resp.usage["total_tokens"] == 0  # Ollama doesn't provide token counts

def test_handle_image_not_implemented():
    req = ImageRequest(provider="ollama", model="llama2", prompt="test")
    with pytest.raises(NotImplementedError):
        adapter.handle_image(req) 