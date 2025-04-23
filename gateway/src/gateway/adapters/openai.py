from gateway.schemas import ChatRequest, ChatResponse, EmbedRequest, EmbedResponse, ImageRequest

def handle_chat(req: ChatRequest) -> ChatResponse:
    # TODO: call OpenAI's API
    # Return a dummy response for now
    return ChatResponse(
        role="assistant",
        content="(stub) chat response not yet implemented",
        name=None,
        finish_reason="stop",
        usage=None,
    )

def stream_chat(req: ChatRequest):
    # TODO: connect to OpenAI with stream=True
    # For now, yield a single SSE chunk and then DONE
    yield "data: (stub) streaming chat start\n\n"
    yield "data: [DONE]\n\n"

def handle_embed(req: EmbedRequest) -> EmbedResponse:
    # TODO: call OpenAI embeddings endpoint
    # Return zero-vectors for each input as a placeholder
    dummy = [[0.0]*4 for _ in req.input]  # 4-dim stub vectors
    return EmbedResponse(embeddings=dummy, usage=None)

def handle_image(req: ImageRequest) -> bytes:
    # TODO: call OpenAI images API
    # Return a 1x1 transparent PNG as stub
    return b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01" \
           b"\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89" \
           b"\x00\x00\x00\nIDATx\x9cc``\x00\x00\x00\x02\x00\x01" \
           b"\xe2!\xbc\x33\x00\x00\x00\x00IEND\xaeB`\x82"