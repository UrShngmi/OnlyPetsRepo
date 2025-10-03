import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import { Product } from '../types';

const ProductsPage: React.FC = () => {
    const { addToCart, addToast } = useAppContext();
    const products: Product[] = [
        { id: 'prod_01', name: 'Organic Pet Food', price: 1500.00, image: 'https://picsum.photos/seed/pet-food/400/400' },
        { id: 'prod_02', name: 'Durable Chew Toy', price: 750.00, image: 'https://picsum.photos/seed/pet-toy/400/400' },
        { id: 'prod_03', name: 'Cozy Pet Bed', price: 2500.00, image: 'https://picsum.photos/seed/pet-bed/400/400' },
        { id: 'prod_04', name: 'Stylish Leash & Collar Set', price: 1200.00, image: 'https://picsum.photos/seed/pet-leash/400/400' },
    ];

    const handleAddToCart = (product: Product) => {
        addToCart(product);
        addToast(`${product.name} added to cart!`, 'success');
    };

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">Pet Products</h1>
        <p className="text-lg text-gray-400">Everything your furry friend needs</p>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
        {products.map((product) => (
            <div key={product.id} className="bg-[#2a2a2a] rounded-2xl overflow-hidden group">
                <img src={product.image} alt={product.name} className="w-full h-56 object-cover transition-transform duration-300 group-hover:scale-105" />
                <div className="p-5">
                    <h3 className="text-xl font-bold text-white">{product.name}</h3>
                    <p className="text-lg text-yellow-400 font-semibold mt-2">₱{product.price.toFixed(2)}</p>
                    <button 
                        onClick={() => handleAddToCart(product)}
                        className="w-full mt-4 bg-yellow-500 text-black font-bold py-2 rounded-lg hover:bg-yellow-400 transition-colors"
                    >
                        Add to Cart
                    </button>
                </div>
            </div>
        ))}
      </div>
    </div>
  );
};

export default ProductsPage;