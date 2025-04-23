import json
import pytest
from gateway.adapters import openai as openai_adapter
from gateway.schemas import ChatResponse, EmbedResponse

@pytest.fixture(autouse=True)
def stub_openai(monkeypatch):
    # stub out handle_chat so routes don't make real HTTP calls
    monkeypatch.setattr(openai_adapter, "handle_chat", lambda req: ChatResponse(
        role="assistant",
        content="test response",
        finish_reason="stop",
        usage={"total_tokens": 1}
    ))
    monkeypatch.setattr(openai_adapter, "stream_chat", lambda req: iter([]))
    monkeypatch.setattr(openai_adapter, "handle_embed", lambda req: EmbedResponse(
        embeddings=[[0.1, 0.2]],
        usage={"total_tokens": 1}
    ))
    monkeypatch.setattr(openai_adapter, "handle_image", lambda req: b"test image data")

def test_chat_route_returns_200(client):
    payload = {
        "provider": "openai",
        "model": "gpt-4o",
        "messages": [{"role": "user", "content": "Hello"}],
    }
    resp = client.post("/chat", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["content"] == "test response"
    assert data["finish_reason"] == "stop"

def test_embed_route_returns_200(client):
    payload = {"provider": "openai", "model": "m", "input": ["a"]}
    resp = client.post("/embed", json=payload)
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["embeddings"] == [[0.1, 0.2]]

def test_image_route_returns_200(client):
    payload = {"provider": "openai", "model": "m", "prompt": "p"}
    resp = client.post("/image", json=payload)
    assert resp.status_code == 200
    assert resp.data == b"test image data"

def test_stream_route_returns_event_stream(client):
    payload = {
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello"}],
        "stream": True,
    }
    resp = client.post("/chat/stream", json=payload)
    assert resp.status_code == 200
    assert resp.mimetype == "text/event-stream" 