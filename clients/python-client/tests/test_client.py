import pytest
from llm_gateway.client import GatewayClient
from llm_gateway.models import ChatResponse

class DummyResponse:
    def __init__(self, status, json_data=None, content=None):
        self.status_code = status
        self._json = json_data or {}
        self.content = content or b""
    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")
    def json(self):
        return self._json

@pytest.fixture
def client(monkeypatch):
    from httpx import Client as HTTPXClient
    dummy = DummyResponse(200, {"role":"assistant","content":"ok","finish_reason":"stop"})
    monkeypatch.setattr(HTTPXClient, "post", lambda self, *a, **k: dummy)
    return GatewayClient(base_url="http://test", api_key="xyz")

def test_chat(client):
    resp = client.chat("m", [{"role":"user","content":"hi"}])
    assert isinstance(resp, ChatResponse)
    assert resp.content == "ok"