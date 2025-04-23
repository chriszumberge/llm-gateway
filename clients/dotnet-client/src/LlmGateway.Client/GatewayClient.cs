using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using LlmGateway.Client.Models;

namespace LlmGateway.Client
{
    public class GatewayClient
    {
        internal HttpClient _http;
        public GatewayClient(string baseUrl, string apiKey)
        {
            _http = new HttpClient
            {
                BaseAddress = new Uri(baseUrl)
            };
            _http.DefaultRequestHeaders.Add("X-API-Key", apiKey);
        }

        public async Task<ChatResponse> ChatAsync(ChatRequest req)
        {
            var resp = await _http.PostAsJsonAsync("/chat", req);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<ChatResponse>()!;
        }

        public async IAsyncEnumerable<string> StreamChatAsync(ChatRequest req)
        {
            req.Stream = true;
            using var request = new HttpRequestMessage(HttpMethod.Post, "/chat/stream")
            {
                Content = JsonContent.Create(req)
            };
            using var response = await _http.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
            response.EnsureSuccessStatusCode();
            using var stream = await response.Content.ReadAsStreamAsync();
            using var reader = new StreamReader(stream);
            while (!reader.EndOfStream)
            {
                var line = await reader.ReadLineAsync();
                if (!string.IsNullOrWhiteSpace(line) && line.StartsWith("data: "))
                    yield return line.Substring(6);
            }
        }

        public async Task<EmbedResponse> EmbedAsync(EmbedRequest req)
        {
            var resp = await _http.PostAsJsonAsync("/embed", req);
            resp.EnsureSuccessStatusCode();
            return await resp.Content.ReadFromJsonAsync<EmbedResponse>()!;
        }

        public async Task<byte[]> GenerateImageAsync(string provider, string model, string prompt, string size="512x512", int n=1, object? parameters=null)
        {
            var payload = new Dictionary<string, object>
            {
                ["provider"] = provider,
                ["model"] = model,
                ["prompt"] = prompt,
                ["size"] = size,
                ["n"] = n
            };
            if (parameters != null) payload["params"] = parameters;

            var response = await _http.PostAsJsonAsync("/image", payload);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsByteArrayAsync();
        }
    }
} 