import httpx
import pytest
from gateway.adapters import anthropic as adapter
from gateway.schemas import ChatRequest, Message, EmbedRequest, ImageRequest

class DummyResponse:
    def __init__(self, json_data, text_data=None):
        self._json = json_data
        self.text = text_data or ""
    def raise_for_status(self): pass
    def json(self): return self._json

def test_handle_chat(monkeypatch):
    fake = {
        "content": [{"text": "hi"}],
        "stop_reason": "stop_sequence",
        "usage": {"input_tokens": 1, "output_tokens": 1}
    }
    monkeypatch.setattr(httpx, "post", lambda *a, **k: DummyResponse(fake))
    req = ChatRequest(provider="anthropic", model="claude-3-opus-20240229", messages=[Message(role="user", content="Hello")])
    resp = adapter.handle_chat(req)
    assert resp.content == "hi"
    assert resp.finish_reason == "stop_sequence"
    assert resp.usage is None

def test_stream_chat(monkeypatch):
    def fake_stream(*args, **kwargs):
        class CM:
            def __enter__(self): return self
            def __exit__(self, *a): pass
            def iter_lines(self, decode_unicode):
                return iter(["data: {\"type\":\"content_block_delta\",\"delta\":{\"text\":\"hello\"}}", "data: [DONE]"])
            def raise_for_status(self): pass
        return CM()
    monkeypatch.setattr(httpx, "stream", fake_stream)
    req = ChatRequest(provider="anthropic", model="claude-3-opus-20240229", messages=[Message(role="user", content="Hello")])
    chunks = list(adapter.stream_chat(req))
    assert "hello" in chunks[0]

def test_handle_embed_not_implemented():
    req = EmbedRequest(provider="anthropic", model="claude-3-opus-20240229", input=["test"])
    with pytest.raises(NotImplementedError):
        adapter.handle_embed(req)

def test_handle_image_not_implemented():
    req = ImageRequest(provider="anthropic", model="claude-3-opus-20240229", prompt="test")
    with pytest.raises(NotImplementedError):
        adapter.handle_image(req) 