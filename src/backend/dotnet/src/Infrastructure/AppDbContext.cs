using EcommerceSystem.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace EcommerceSystem.Infrastructure
{
    public class AppDbContext : DbContext
    {
        public DbSet<Product> Products { get; set; }

        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
    }
}