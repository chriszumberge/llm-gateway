from flask import Blueprint, request, jsonify, Response
from gateway.schemas import ChatRequest, EmbedRequest, ImageRequest
from gateway.adapters import openai as openai_adapter
from gateway.adapters import azure as azure_adapter
from gateway.adapters import anthropic as anthropic_adapter
from gateway.adapters import bedrock as bedrock_adapter
from gateway.adapters import ollama as ollama_adapter

router = Blueprint("api", __name__)

def _get_adapter(provider: str):
    return {
        "openai": openai_adapter,
        "azure": azure_adapter,
        "anthropic": anthropic_adapter,
        "bedrock": bedrock_adapter,
        "ollama": ollama_adapter,
    }[provider]

@router.route("/chat", methods=["POST"])
def chat():
    # Validate incoming JSON against our Pydantic model
    req = ChatRequest.parse_obj(request.get_json())
    # Get the appropriate adapter based on provider
    adapter = _get_adapter(req.provider)
    resp = adapter.handle_chat(req)
    # Return standardized JSON
    return jsonify(resp.dict())

@router.route("/chat/stream", methods=["POST"])
def chat_stream():
    req = ChatRequest.parse_obj(request.get_json())
    adapter = _get_adapter(req.provider)
    # This should be a generator of SSE-formatted data
    return Response(
        adapter.stream_chat(req),
        mimetype="text/event-stream",
    )

@router.route("/embed", methods=["POST"])
def embed():
    req = EmbedRequest.parse_obj(request.get_json())
    adapter = _get_adapter(req.provider)
    resp = adapter.handle_embed(req)
    return jsonify(resp.dict())

@router.route("/image", methods=["POST"])
def image():
    req = ImageRequest.parse_obj(request.get_json())
    adapter = _get_adapter(req.provider)
    # Return raw image bytes
    image_bytes = adapter.handle_image(req)
    return Response(image_bytes, mimetype="image/png") 