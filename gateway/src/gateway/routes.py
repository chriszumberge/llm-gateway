from flask import Blueprint, request, jsonify, Response
from gateway.schemas import ChatRequest, EmbedRequest, ImageRequest
from gateway.adapters import openai as openai_adapter

router = Blueprint("api", __name__)

@router.route("/chat", methods=["POST"])
def chat():
    # Validate incoming JSON against our Pydantic model
    req = ChatRequest.parse_obj(request.get_json())
    # For now, dispatch to OpenAI adapter stub
    resp = openai_adapter.handle_chat(req)
    # Return standardized JSON
    return jsonify(resp.dict())

@router.route("/chat/stream", methods=["POST"])
def chat_stream():
    req = ChatRequest.parse_obj(request.get_json())
    # This should be a generator of SSE-formatted data
    return Response(
        openai_adapter.stream_chat(req),
        mimetype="text/event-stream",
    )

@router.route("/embed", methods=["POST"])
def embed():
    req = EmbedRequest.parse_obj(request.get_json())
    resp = openai_adapter.handle_embed(req)
    return jsonify(resp.dict())

@router.route("/image", methods=["POST"])
def image():
    req = ImageRequest.parse_obj(request.get_json())
    # Return raw image bytes
    image_bytes = openai_adapter.handle_image(req)
    return Response(image_bytes, mimetype="image/png") 