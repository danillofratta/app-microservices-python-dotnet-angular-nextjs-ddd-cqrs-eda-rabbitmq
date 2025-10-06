using Domain.repositoreis;
using EcommerceSystem.Domain.Entities;
using EcommerceSystem.Domain.Events;
using MassTransit;

namespace EcommerceSystem.Application.Commands
{
    public class ReserveStockResult
    {
        public bool Success { get; set; }
        public string? Message { get; set; }
    }
}
