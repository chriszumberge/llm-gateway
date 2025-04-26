using LlmGateway.Client;
using LlmGateway.Client.Models;

// Simple console app that calls the running gateway
class Program
{
    static async Task Main()
    {
        // Gateway base URL in Docker Compose CI
        var baseUrl = "http://localhost:8000";
        var apiKey  = "dummy-key"; // Gateway doesn't require auth by default

        var client = new GatewayClient(baseUrl, apiKey);
        var request = new ChatRequest
        {
            Provider = "openai", // provider name is required but mocked in gateway when no key
            Model = "gpt-3.5-turbo",
            Messages = new() { new Message { Role = "user", Content = "Hello from .NET example!" } }
        };

        var response = await client.ChatAsync(request);
        Console.WriteLine($"Assistant: {response.Content}");
    }
} 