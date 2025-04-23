import axios, { AxiosInstance } from "axios";
import {
  ChatRequest,
  ChatResponse,
  EmbedRequest,
  EmbedResponse,
  ImageRequest,
} from "./types";

export class LlmGatewayClient {
  private http: AxiosInstance;

  constructor(baseURL: string, apiKey: string, timeout = 30000) {
    this.http = axios.create({
      baseURL,
      timeout,
      headers: {
        "Content-Type": "application/json",
        "X-API-Key": apiKey,
      },
    });
  }

  // ——— Chat ———
  async chat(request: ChatRequest): Promise<ChatResponse> {
    const resp = await this.http.post<ChatResponse>("/chat", request);
    return resp.data;
  }

  // Streaming chat via EventSource (SSE)
  streamChat(
    request: ChatRequest,
    onData: (chunk: string) => void,
    onError?: (err: any) => void,
    onComplete?: () => void
  ): EventSource {
    // Ensure stream=true
    const q = new URLSearchParams();
    request.stream = true;
    const es = new EventSource(
      // SSE over `/chat/stream` with payload in query is nonstandard—
      // instead we open fetch and hook stream manually:
      // Here's a minimal workaround:
      this.http
        .post("/chat/stream", request, { responseType: "stream" })
        .then((response) => {
          const reader = response.data.getReader();
          const decoder = new TextDecoder();
          function read() {
            reader.read().then(({ done, value }: { done: boolean; value: Uint8Array }) => {
              if (done) {
                onComplete?.();
                return;
              }
              const chunk = decoder.decode(value);
              onData(chunk);
              read();
            });
          }
          read();
        })
        .catch(onError)
        .then(() => onComplete?.())
        .toString() // SSE is bypassed; we just return a dummy ES
    );
    return es;
  }

  // ——— Embedding ———
  async embed(request: EmbedRequest): Promise<EmbedResponse> {
    const resp = await this.http.post<EmbedResponse>("/embed", request);
    return resp.data;
  }

  // ——— Image ———
  async generateImage(request: ImageRequest): Promise<ArrayBuffer> {
    const resp = await this.http.post("/image", request, {
      responseType: "arraybuffer",
    });
    return resp.data;
  }
} 