namespace LlmGateway.Client.Models
{
    public class EmbedRequest
    {
        public string Provider { get; set; } = default!;
        public string Model { get; set; } = default!;
        public List<string> Input { get; set; } = new();
    }
} 