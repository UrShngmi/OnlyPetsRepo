import React from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import HomePage from './pages/HomePage';
import AdoptionPage from './pages/AdoptionPage';
import PetDetailsPage from './pages/PetDetailsPage';
import ServicesPage from './pages/ServicesPage';
import ProductsPage from './pages/ProductsPage';
import ContactPage from './pages/ContactPage';
import WishlistPage from './pages/WishlistPage';
import AuthModal from './components/AuthModal';
import ToastContainer from './components/ToastContainer';
import CartPage from './pages/CartPage';
import BookingPage from './pages/BookingPage';
import ProfileSetupModal from './components/ProfileSetupModal';

const App: React.FC = () => {
  return (
    <HashRouter>
      <div className="bg-[#1c1c1c] text-white min-h-screen font-sans">
        <div className="bg-black bg-opacity-30 backdrop-blur-sm sticky top-0 z-40">
            <div className="container mx-auto px-4 max-w-7xl">
                <Header />
            </div>
        </div>
        <main className="container mx-auto px-4 py-8 max-w-7xl">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/adoption" element={<AdoptionPage />} />
            <Route path="/adoption/:petId" element={<PetDetailsPage />} />
            <Route path="/services" element={<ServicesPage />} />
            <Route path="/products" element={<ProductsPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/wishlist" element={<WishlistPage />} />
            <Route path="/cart" element={<CartPage />} />
            <Route path="/booking/:type/:id" element={<BookingPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <AuthModal />
        <ProfileSetupModal />
        <ToastContainer />
      </div>
    </HashRouter>
  );
};

export default App;