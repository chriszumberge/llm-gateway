using System;
using System.Threading.Tasks;
using LlmGateway.Client;
using LlmGateway.Client.Models;

class Program
{
    static async Task Main()
    {
        var client = new GatewayClient("http://localhost:8000", "YOUR_KEY");
        var req = new ChatRequest {
            Provider = "openai",
            Model = "gpt-3.5-turbo",
            Messages = new [] { new Message { Role="user", Content="Hello from .NET!" } }
        };
        var resp = await client.ChatAsync(req);
        Console.WriteLine("Assistant: " + resp.Content);
    }
} 