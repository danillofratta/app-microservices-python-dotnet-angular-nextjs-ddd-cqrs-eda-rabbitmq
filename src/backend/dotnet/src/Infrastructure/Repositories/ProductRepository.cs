using Domain.repositoreis;
using EcommerceSystem.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace EcommerceSystem.Infrastructure.Repositories
{


    public class ProductRepository : IProductRepository
    {
        private readonly AppDbContext _context;

        public ProductRepository(AppDbContext context)
        {
            _context = context;
        }

        public async Task<Product> GetByIdAsync(Guid id)
        {
            return await _context.Products.FindAsync(id);
        }

        public async Task UpdateAsync(Product product)
        {
            _context.Products.Update(product);
            await _context.SaveChangesAsync();
        }

        public async Task<List<Product>> GetAllAsync()
        {            
            return await _context.Products.ToListAsync();
        }
    }
}