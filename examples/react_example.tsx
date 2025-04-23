import React, { useEffect, useState } from "react";
import { LlmGatewayClient, ChatRequest } from "@yourorg/llm-gateway-client";

const client = new LlmGatewayClient("http://localhost:8000", "YOUR_KEY");

export function App() {
  const [response, setResponse] = useState("");
  useEffect(() => {
    const req: ChatRequest = {
      provider: "openai",
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: "Hello from React!" }],
    };
    client.chat(req).then(r => setResponse(r.content));
  }, []);
  return <div><h1>Assistant says:</h1><p>{response}</p></div>;
} 