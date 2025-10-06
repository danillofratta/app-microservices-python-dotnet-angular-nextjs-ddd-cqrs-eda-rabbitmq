import { useEffect, useState } from 'react';

export default function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:61362/api/products')
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  const addProduct = async () => {
    const product = { name: 'New Product', price: 20.0, stock: 100 };
    await fetch('http://localhost:61362/api/products/reserve-stock', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    });
  };

  return (
    <div>
      <h1>Products</h1>
      {products.map(product => (
        <div key={product.id}>{product.name} - Stock: {product.stock}</div>
      ))}
      <button onClick={addProduct}>Add Product</button>
    </div>
  );
}