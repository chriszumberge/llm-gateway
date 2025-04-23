import io
import json
import pytest
from gateway.adapters import bedrock as adapter
from gateway.schemas import ChatRequest, Message, EmbedRequest, ImageRequest

class DummyClient:
    def __init__(self, **methods): 
        self.__dict__.update(methods)

@pytest.fixture(autouse=True)
def stub_bedrock(monkeypatch):
    client = DummyClient(
        converse=lambda **kw: {
            "modelOutputs":[{"content":"hi","stopReason":"stop"}],
            "usage":{"total_tokens":1}
        },
        invoke_model=lambda **kw: {
            "body": io.BytesIO(json.dumps({"embeddings":[[0.5,0.6]]}).encode())
        }
    )
    monkeypatch.setattr(adapter, "bedrock", client)

def test_handle_chat_bedrock():
    req = ChatRequest(provider="bedrock", model="anthropic.claude-3-sonnet-20240229-v1:0", messages=[Message(role="user", content="Hi")])
    resp = adapter.handle_chat(req)
    assert resp.content == "hi"
    assert resp.finish_reason == "stop"
    assert resp.usage["total_tokens"] == 1

def test_handle_embed_bedrock():
    req = EmbedRequest(provider="bedrock", model="amazon.titan-embed-text-v1", input=["test"])
    resp = adapter.handle_embed(req)
    assert resp.embeddings == [[0.5,0.6]]

def test_handle_image_bedrock():
    img_bytes = b"\x89PNG"
    # override invoke_model to return image bytes
    adapter.bedrock.invoke_model = lambda **kw: {"body": io.BytesIO(img_bytes)}
    req = ImageRequest(provider="bedrock", model="stability.stable-diffusion-xl-v1", prompt="test")
    assert adapter.handle_image(req) == img_bytes 