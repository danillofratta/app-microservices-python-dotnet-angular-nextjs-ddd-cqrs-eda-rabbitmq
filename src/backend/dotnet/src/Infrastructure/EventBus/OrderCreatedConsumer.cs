using EcommerceSystem.Application.Commands;
using MassTransit;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace EcommerceSystem.Infrastructure.EventBus;

    public class OrderCreatedConsumer : IConsumer<Order>
    {
        private readonly ReserveStockCommandHandler _handler;

        public OrderCreatedConsumer(ReserveStockCommandHandler handler)
        {
            _handler = handler;
        }

        public async Task Consume(ConsumeContext<Order> context)
        {
            var message = context.Message;

            var command = new ReserveStockCommand
            {
                OrderId = Guid.Parse(context.Message.OrderId), // or message.OrderId if using JsonPropertyName
                Items = context.Message.Items.Select(item => new ProductCommand
                {
                    Id = Guid.Parse(item.Id), // or item.ProductId if using JsonPropertyName
                    Quantity = item.Quantity // or item.Quantity
                }).ToList()
            };

            await _handler.HandleAsync(command);
        }
    }

public class Order
{
    [JsonPropertyName("order_id")]
    public string OrderId { get; set; }

    [JsonPropertyName("customer_id")]
    public string CustomerId { get; set; }

    [JsonPropertyName("items")]
    public List<Item> Items { get; set; }

    [JsonPropertyName("total")]
    public decimal Total { get; set; }
}

public class Item
{
    [JsonPropertyName("id")]
    public string Id { get; set; }

    [JsonPropertyName("quantity")]
    public int Quantity { get; set; }

    [JsonPropertyName("price")]
    public decimal Price { get; set; }
}