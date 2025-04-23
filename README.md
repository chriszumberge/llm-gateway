# Universal LLM Gateway

A stateless, provider-agnostic gateway for chat, embeddings, image generation, and function/tool calling across:

- **OpenAI**  
- **Azure OpenAI Service**  
- **Anthropic Claude**  
- **AWS Bedrock**  
- **Ollama**

Clients available in Python, .NET 8, and TypeScript/React.

---

## Quickstart

### 1. Run the Gateway

```bash
# from repo root
cd gateway
docker compose up -d
```

Gateway listens on `http://localhost:8000`.

### 2. Chat with `curl`

```bash
curl http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "messages": [{ "role": "user", "content": "Hello!" }]
  }'
```

### 3. Embed

```bash
curl http://localhost:8000/embed \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model": "text-embedding-ada-002",
    "input": ["foo", "bar"]
  }'
```

### 4. Generate an Image

```bash
curl http://localhost:8000/image \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "openai",
    "model": "dall-e-3",
    "prompt": "A fox in a forest",
    "size": "512x512",
    "n": 1
  }' --output fox.png
```

---

## Examples

See the **examples/** folder for minimal scripts showing how to call the gateway from each client:

- `examples/python_example.py`  
- `examples/dotnet_example.cs`  
- `examples/react_example.tsx`  

Run them after installing the respective client library.

---

## Client Libraries

### Python

See [clients/python-client/README.md](clients/python-client/README.md) for install & usage.

```bash
pip install llm-gateway-client
```

### .NET

See [clients/dotnet-client/README.md](clients/dotnet-client/README.md):

```bash
dotnet add package LlmGateway.Client
```

### React / TypeScript

See [clients/react-client/README.md](clients/react-client/README.md):

```bash
npm install @yourorg/llm-gateway-client
```

---

## Configuration

Copy `.env.example` → `.env` under **gateway/** and fill in:

```dotenv
OPENAI_API_KEY=…
AZURE_OPENAI_ENDPOINT=https://…
AZURE_OPENAI_KEY=…
AZURE_OPENAI_API_VERSION=…
ANTHROPIC_API_KEY=…
ANTHROPIC_API_VERSION=…
AWS_ACCESS_KEY_ID=…
AWS_SECRET_ACCESS_KEY=…
AWS_DEFAULT_REGION=…
OLLAMA_API_URL=http://localhost:11434/api
```

---

## Development

- **Tests**  
  ```bash
  # Gateway
  cd gateway && poetry run pytest

  # Python client
  cd clients/python-client && poetry run pytest

  # .NET client
  cd clients/dotnet-client && dotnet test

  # React client
  cd clients/react-client && npm test
  ```

- **Linting & Formatting**  
  Add your preferred linters to each sub-project.

---

## Roadmap

1. Async job endpoints & polling  
2. Server-side session context (optional)  
3. Tool execution plugins  
4. Monitoring, metrics, health endpoints  

---

## Contribute

Please open issues or PRs! All feedback welcome.