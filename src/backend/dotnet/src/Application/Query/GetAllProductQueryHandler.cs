using Domain.repositoreis;

namespace Appication.Query;
public class GetAllProductQueryHandler 
{
    private readonly IProductRepository _repository;    
    public GetAllProductQueryHandler(IProductRepository repository)
    {
        _repository = repository;        
    }

    public async Task<List<GetAllProductQueryResult>> HandleAsync()
    {
        var products = await _repository.GetAllAsync();

        List<GetAllProductQueryResult> list = new List<GetAllProductQueryResult>();
        foreach (var item in products)
        {
            var additem = new GetAllProductQueryResult
            {
                Id = item.Id,
                Name = item.Name,
                Price = item.Price,
                Stock = item.Stock,
            };
            list.Add(additem);
        }

        return list;
    }
}


