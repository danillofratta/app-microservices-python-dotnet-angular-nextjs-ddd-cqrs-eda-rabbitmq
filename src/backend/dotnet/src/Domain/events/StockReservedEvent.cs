using System.Text.Json.Serialization;

namespace EcommerceSystem.Domain.Events;

public class StockReservedEvent
{
    [JsonPropertyName("order_id")] // Mapeia para snake_case
    public string OrderId { get; set; } = string.Empty;
    [JsonPropertyName("success")]
    public bool Success { get; set; }
}