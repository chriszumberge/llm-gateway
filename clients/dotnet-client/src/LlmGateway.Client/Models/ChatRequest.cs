namespace LlmGateway.Client.Models
{
    public class Message
    {
        public string Role { get; set; } = default!;
        public string? Name { get; set; }
        public string Content { get; set; } = default!;
    }

    public class FunctionDef
    {
        public string Name { get; set; } = default!;
        public string Description { get; set; } = default!;
        public object Parameters { get; set; } = default!; // JSON Schema
    }

    public class ChatRequest
    {
        public string Provider { get; set; } = default!;
        public string Model { get; set; } = default!;
        public List<Message> Messages { get; set; } = new();
        public List<FunctionDef>? Functions { get; set; }
        public double Temperature { get; set; } = 1.0;
        public int? MaxTokens { get; set; }
        public double TopP { get; set; } = 1.0;
        public bool Stream { get; set; } = false;
    }
} 