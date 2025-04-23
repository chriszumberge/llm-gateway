namespace LlmGateway.Client.Models
{
    public class EmbedResponse
    {
        public List<List<double>> Embeddings { get; set; } = new();
        public object? Usage { get; set; }
    }
} 