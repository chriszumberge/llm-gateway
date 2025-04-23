// —— Common primitives ——
export type Role = "system" | "user" | "assistant" | "function" | "tool";

export interface Message {
  role: Role;
  name?: string;
  content: string;
}

export interface FunctionDef {
  name: string;
  description: string;
  parameters: Record<string, any>; // JSON Schema
}

// —— Chat ——
export interface ChatRequest {
  provider: "openai" | "azure" | "anthropic" | "bedrock" | "ollama";
  model: string;
  messages: Message[];
  functions?: FunctionDef[];
  temperature?: number;
  max_tokens?: number;
  top_p?: number;
  stream?: boolean;
}

export interface ChatResponse {
  role: string;
  content: string;
  name?: string;
  finish_reason?: string;
  usage?: any;
}

// —— Embeddings ——
export interface EmbedRequest {
  provider: "openai" | "azure" | "bedrock" | "ollama";
  model: string;
  input: string[];
}

export interface EmbedResponse {
  embeddings: number[][];
  usage?: any;
}

// —— Image ——
export interface ImageRequest {
  provider: "openai" | "azure" | "bedrock";
  model: string;
  prompt: string;
  size?: "256x256" | "512x512" | "1024x1024";
  n?: number;
  params?: Record<string, any>;
} 