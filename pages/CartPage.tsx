import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import { Link } from 'react-router-dom';

const CartPage: React.FC = () => {
  const { cart, removeFromCart, updateCartQuantity, addToast, clearCart } = useAppContext();

  const subtotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const taxes = subtotal * 0.1; // 10% tax
  const total = subtotal + taxes;

  const handleCheckout = () => {
    addToast('Checkout successful! Thank you for your order. (Simulated)', 'success');
    clearCart();
  }

  if (cart.length === 0) {
    return (
      <div className="text-center py-16 bg-[#2a2a2a] rounded-2xl">
        <h1 className="text-3xl font-bold text-white mb-4">Your Cart is Empty</h1>
        <p className="text-gray-400 mb-6">Looks like you haven't added anything to your cart yet.</p>
        <Link 
          to="/products"
          className="inline-block bg-yellow-500 text-black font-bold py-3 px-8 rounded-lg hover:bg-yellow-400 transition-all"
        >
          Browse Products
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">Your Cart</h1>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div className="lg:col-span-2 bg-[#121212] p-8 rounded-3xl space-y-4">
          <h2 className="text-2xl font-bold mb-4 border-b border-gray-700 pb-4">Cart Items</h2>
          {cart.map(item => (
            <div key={item.id} className="flex flex-col sm:flex-row items-center bg-[#2a2a2a] p-4 rounded-xl gap-4">
              <img src={item.image} alt={item.name} className="w-24 h-24 object-cover rounded-md" />
              <div className="flex-grow text-center sm:text-left">
                <h3 className="text-lg font-bold text-white">{item.name}</h3>
                <p className="text-yellow-400">₱{item.price.toFixed(2)}</p>
              </div>
              <div className="flex items-center space-x-3">
                <button onClick={() => updateCartQuantity(item.id, item.quantity - 1)} className="px-3 py-1 bg-gray-700 rounded-md hover:bg-gray-600">-</button>
                <span className="w-8 text-center">{item.quantity}</span>
                <button onClick={() => updateCartQuantity(item.id, item.quantity + 1)} className="px-3 py-1 bg-gray-700 rounded-md hover:bg-gray-600">+</button>
              </div>
              <p className="text-lg font-semibold w-24 text-right mx-4">₱{(item.price * item.quantity).toFixed(2)}</p>
              <button onClick={() => removeFromCart(item.id)} className="text-2xl text-gray-400 hover:text-red-500">&times;</button>
            </div>
          ))}
        </div>
        <div className="bg-[#121212] p-8 rounded-3xl self-start">
          <h2 className="text-2xl font-bold mb-6">Order Summary</h2>
          <div className="space-y-3 text-gray-300">
            <div className="flex justify-between">
              <p>Subtotal</p>
              <p>₱{subtotal.toFixed(2)}</p>
            </div>
            <div className="flex justify-between">
              <p>Taxes (10%)</p>
              <p>₱{taxes.toFixed(2)}</p>
            </div>
            <div className="border-t border-gray-700 my-4"></div>
            <div className="flex justify-between text-white font-bold text-xl">
              <p>Total</p>
              <p>₱{total.toFixed(2)}</p>
            </div>
          </div>
          <button 
            onClick={handleCheckout}
            className="w-full mt-6 bg-yellow-500 text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition-colors"
          >
            Proceed to Checkout
          </button>
        </div>
      </div>
    </div>
  );
};

export default CartPage;