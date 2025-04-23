using System.Net;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;
using LlmGateway.Client;
using LlmGateway.Client.Models;
using NUnit.Framework;
using Moq;
using Moq.Protected;

namespace LlmGateway.Client.Tests
{
    public class GatewayClientTests
    {
        private const string BaseUrl = "http://test";
        private const string ApiKey = "key";

        private GatewayClient CreateClient(HttpResponseMessage fakeResponse)
        {
            var handlerMock = new Mock<HttpMessageHandler>();
            handlerMock
                .Protected()
                .Setup<Task<HttpResponseMessage>>("SendAsync",
                    ItExpr.IsAny<HttpRequestMessage>(),
                    ItExpr.IsAny<CancellationToken>())
                .ReturnsAsync(fakeResponse);

            var http = new HttpClient(handlerMock.Object) { BaseAddress = new Uri(BaseUrl) };
            http.DefaultRequestHeaders.Add("X-API-Key", ApiKey);
            var client = new GatewayClient(BaseUrl, ApiKey);
            client._http = http;
            return client;
        }

        [Test]
        public async Task ChatAsync_ReturnsResponse()
        {
            var dummy = new ChatResponse { Role="assistant", Content="ok", FinishReason="stop" };
            var fake = new HttpResponseMessage(HttpStatusCode.OK)
            {
                Content = JsonContent.Create(dummy)
            };
            var client = CreateClient(fake);
            var req = new ChatRequest { Provider="openai", Model="m", Messages=new List<Message>{ new(){ Role="user", Content="hi" } } };
            var resp = await client.ChatAsync(req);
            Assert.That(resp.Content, Is.EqualTo("ok"));
            Assert.That(resp.Role, Is.EqualTo("assistant"));
        }

        [Test]
        public async Task EmbedAsync_ReturnsEmbeddings()
        {
            var dummy = new EmbedResponse { Embeddings = new List<List<double>>{ new(){1.0,2.0} } };
            var fake = new HttpResponseMessage(HttpStatusCode.OK){
                Content = JsonContent.Create(dummy)
            };
            var client = CreateClient(fake);
            var req = new EmbedRequest { Provider="openai", Model="m", Input=new List<string>{"a"} };
            var resp = await client.EmbedAsync(req);
            Assert.That(resp.Embeddings.Count, Is.EqualTo(1));
            Assert.That(resp.Embeddings[0][1], Is.EqualTo(2.0));
        }

        // ... you can add streaming and image tests similarly ...
    }
} 