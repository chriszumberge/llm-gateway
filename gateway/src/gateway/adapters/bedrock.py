import json
import boto3
from gateway.schemas import ChatRequest, ChatResponse, EmbedRequest, EmbedResponse, ImageRequest

# Initialize Bedrock client
bedrock = boto3.client("bedrock")  # region from AWS env/config

def handle_chat(req: ChatRequest) -> ChatResponse:
    # Use the Converse API for chat-capable models
    response = bedrock.converse(
        modelId=req.model,
        messages=[m.dict(exclude_none=True) for m in req.messages],
        temperature=req.temperature,
        maxTokens=req.max_tokens,
        topP=req.top_p,
    )
    # response['modelOutputs'][0]['content'] has the assistant reply
    content = response["modelOutputs"][0]["content"]
    finish = response["modelOutputs"][0].get("stopReason")
    # usage under response['usage']
    usage = response.get("usage")
    return ChatResponse(
        role="assistant",
        content=content,
        name=None,
        finish_reason=finish,
        usage=usage,
    )

def stream_chat(req: ChatRequest):
    # streaming via converse() with stream=True
    stream = bedrock.converse(
        modelId=req.model,
        messages=[m.dict(exclude_none=True) for m in req.messages],
        temperature=req.temperature,
        maxTokens=req.max_tokens,
        topP=req.top_p,
        stream=True,
    )
    for event in stream:
        # each event has 'content'
        chunk = event["modelOutputs"][0]["content"]
        yield f"data: {chunk}\n\n"

def handle_embed(req: EmbedRequest) -> EmbedResponse:
    # Titan Embeddings or other embedding model
    response = bedrock.invoke_model(
        modelId=req.model,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": req.input}),
    )
    payload = json.loads(response["body"].read())
    vectors = payload["embeddings"]
    # Bedrock may not return usage
    return EmbedResponse(embeddings=vectors, usage=None)

def handle_image(req: ImageRequest) -> bytes:
    # Stable Diffusion via InvokeModel with Accept header image/png
    response = bedrock.invoke_model(
        modelId=req.model,
        contentType="application/json",
        accept="image/png",
        body=json.dumps({
            "text_prompts": [{"text": req.prompt}],
            "height": int(req.size.split("x")[0]),
            "width": int(req.size.split("x")[1]),
        })
    )
    # response['body'] is a StreamingBody, read raw bytes
    return response["body"].read() 