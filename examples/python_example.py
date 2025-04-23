from llm_gateway.client import GatewayClient

client = GatewayClient("http://localhost:8000", api_key="YOUR_KEY")

resp = client.chat(
    model="gpt-3.5-turbo",
    messages=[{"role":"user","content":"Hello from Python!"}]
)
print("Assistant:", resp.content) 