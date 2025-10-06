using Appication.Query;
using EcommerceSystem.Application.Commands;
using Microsoft.AspNetCore.Mvc;
using System.Threading.Tasks;
using static MassTransit.ValidationResultExtensions;

namespace EcommerceSystem.Api.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class ProductsController : ControllerBase
    {
        private readonly ReserveStockCommandHandler _reservestockcommadhandler;
        private readonly GetAllProductQueryHandler _productqueryhandler;

        public ProductsController(ReserveStockCommandHandler reservestockcommadhandler, GetAllProductQueryHandler productqueryhandler)
        {
            _reservestockcommadhandler = reservestockcommadhandler;
            _productqueryhandler = productqueryhandler;
        }

        [HttpPost("reserve-stock")]
        public async Task<IActionResult> ReserveStock([FromBody] ReserveStockCommand command)
        {
            try
            {
                var result = await _reservestockcommadhandler.HandleAsync(command);

                if (result.Success)
                    return Ok(result);

                return BadRequest(result);
            }
            catch (System.Exception ex)
            {
                return BadRequest(ex);
            }
        }

        [HttpGet]
        public async Task<IActionResult> GetAllProducts()
        {
            try
            {
                var result = await _productqueryhandler.HandleAsync();
                
            return Ok(result);
            }
            catch (System.Exception ex)
            {
                return BadRequest(ex);                
            }                       
        }
    }
}
