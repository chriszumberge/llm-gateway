namespace LlmGateway.Client.Models
{
    public class ChatResponse
    {
        public string Role { get; set; } = default!;
        public string Content { get; set; } = default!;
        public string? Name { get; set; }
        public string? FinishReason { get; set; }
        public object? Usage { get; set; }
    }
} 