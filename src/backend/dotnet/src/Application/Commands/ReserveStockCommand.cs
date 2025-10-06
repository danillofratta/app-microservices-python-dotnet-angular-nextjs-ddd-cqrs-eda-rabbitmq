using Domain.repositoreis;
using EcommerceSystem.Domain.Entities;
using EcommerceSystem.Domain.Events;
using MassTransit;

namespace EcommerceSystem.Application.Commands
{
    public class ReserveStockCommand
    {
        public Guid OrderId { get; set; }
        public List<ProductCommand> Items { get; set; }
    }

    public class ProductCommand
    {
        public Guid Id { get; set; } 
        public int Quantity { get; set; } = 0;
    }
}