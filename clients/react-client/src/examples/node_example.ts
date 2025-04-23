import { LlmGatewayClient } from "../client";

(async () => {
  const client = new LlmGatewayClient("http://localhost:8000", "YOUR_KEY");
  const resp = await client.chat({
    provider: "openai",
    model: "gpt-3.5-turbo",
    messages: [{ role: "user", content: "Hello from Node!" }],
  });
  console.log("Assistant:", resp.content);
})(); 