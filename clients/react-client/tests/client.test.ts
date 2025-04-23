import { LlmGatewayClient } from "../src/client";
import { ChatRequest } from "../src/types";
import axios, { AxiosInstance } from "axios";

jest.mock("axios");
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe("LlmGatewayClient", () => {
  let client: LlmGatewayClient;
  let mockAxiosInstance: jest.Mocked<AxiosInstance>;

  beforeEach(() => {
    // Reset all mocks before each test
    jest.clearAllMocks();
    
    // Create a mock axios instance
    mockAxiosInstance = {
      post: jest.fn(),
    } as unknown as jest.Mocked<AxiosInstance>;

    // Set up axios.create to return our mock instance
    mockedAxios.create.mockReturnValue(mockAxiosInstance);

    // Create a new client instance after setting up the mock
    client = new LlmGatewayClient("http://test", "key");
  });

  it("chat() should return data", async () => {
    const mockResponse = { data: { role: "assistant", content: "ok" } };
    mockAxiosInstance.post.mockResolvedValue(mockResponse);

    const req: ChatRequest = {
      provider: "openai",
      model: "m",
      messages: [{ role: "user", content: "hello" }],
    };
    const resp = await client.chat(req);
    expect(resp.content).toBe("ok");
    expect(mockAxiosInstance.post).toHaveBeenCalledWith("/chat", req);
  });
}); 