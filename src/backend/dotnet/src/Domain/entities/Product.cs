using System;

namespace EcommerceSystem.Domain.Entities
{
    public class Product
    {
        public Guid Id { get; private set; }
        public string Name { get; private set; }
        public decimal Price { get; private set; }
        public int Stock { get; private set; }

        public Product(string name, decimal price, int stock)
        {
            Id = Guid.NewGuid();
            Name = name;
            Price = price;
            Stock = stock;
        }

        public bool ReserveStock(int quantity)
        {
            if (Stock >= quantity)
            {
                Stock -= quantity;
                return true;
            }
            return false;
        }
    }
}