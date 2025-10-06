using EcommerceSystem.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.repositoreis;

public interface IProductRepository
{
    Task<Product> GetByIdAsync(Guid id);

    Task<List<Product>> GetAllAsync();
    Task UpdateAsync(Product product);
}