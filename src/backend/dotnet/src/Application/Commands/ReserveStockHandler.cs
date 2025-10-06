using Domain.repositoreis;
using EcommerceSystem.Domain.Events;
using MassTransit;
using System.Text.Json;

namespace EcommerceSystem.Application.Commands
{
    public class ReserveStockCommandHandler
    {
        private readonly IProductRepository _repository;
        private readonly IBus _publishEndpoint;

        public ReserveStockCommandHandler(IProductRepository repository, IBus publishEndpoint)
        {
            _repository = repository;
            _publishEndpoint = publishEndpoint;
        }

        public async Task<ReserveStockResult> HandleAsync(ReserveStockCommand command)
        {
            bool success = true;

            foreach (var item in command.Items)
            {
                var product = await _repository.GetByIdAsync(item.Id);
                if (product == null || !product.ReserveStock(item.Quantity))
                {
                    success = false;
                    break;
                }

                await _repository.UpdateAsync(product);
            }

            var message = new StockReservedEvent
            {
                OrderId = command.OrderId.ToString(),
                Success = success
            };

            await _publishEndpoint.Publish(message, context =>
            {
                context.SetRoutingKey("stock.reserved");
            });                        

            return new ReserveStockResult
            {
                Success = success,
                Message = success ? "Stock reserved successfully" : "Stock reservation failed"
            };
        }
    }
}
