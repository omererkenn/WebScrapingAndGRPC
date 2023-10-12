// See https://aka.ms/new-console-template for more information
using Grpc.Net.Client;

var handler = new HttpClientHandler();
handler.ServerCertificateCustomValidationCallback = 
    HttpClientHandler.DangerousAcceptAnyServerCertificateValidator;

var channel = GrpcChannel.ForAddress("http://localhost:8080",
    new GrpcChannelOptions { HttpHandler = handler });
var client = new ScrapeService.ScrapeServiceClient(channel);

var reply =  client.ProductResponse(new ProductRequest());
Console.WriteLine(reply);
Console.WriteLine("Press any key to exit...");
Console.ReadKey();


