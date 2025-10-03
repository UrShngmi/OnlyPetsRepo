import React, { useState, useEffect, useRef } from 'react';
import { NavLink } from 'react-router-dom';
import { useAppContext } from '../contexts/AppContext';

const Header: React.FC = () => {
  const { wishlist, cart, toggleAuthModal, currentUser, logout } = useAppContext();
  const [isDropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const linkClass = "text-gray-300 hover:text-white transition-colors duration-300 px-3 py-2 rounded-md text-sm font-medium";
  const activeLinkClass = "text-white bg-yellow-600 bg-opacity-20";
  const totalCartItems = cart.reduce((sum, item) => sum + item.quantity, 0);

  const handleLogout = () => {
    logout();
    setDropdownOpen(false);
  }

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <header className="py-4">
      <nav className="flex items-center justify-between">
        <NavLink to="/" className="text-2xl font-bold text-yellow-500 tracking-wider">
          ONLYPETS
        </NavLink>
        <div className="hidden md:flex items-center space-x-2">
          <NavLink to="/" className={({ isActive }) => isActive ? `${linkClass} ${activeLinkClass}` : linkClass}>Home</NavLink>
          <NavLink to="/adoption" className={({ isActive }) => isActive ? `${linkClass} ${activeLinkClass}` : linkClass}>Adoption</NavLink>
          <NavLink to="/services" className={({ isActive }) => isActive ? `${linkClass} ${activeLinkClass}` : linkClass}>Services</NavLink>
          <NavLink to="/products" className={({ isActive }) => isActive ? `${linkClass} ${activeLinkClass}` : linkClass}>Products</NavLink>
          <NavLink to="/contact" className={({ isActive }) => isActive ? `${linkClass} ${activeLinkClass}` : linkClass}>Contact</NavLink>
        </div>
        <div className="flex items-center space-x-4">
          <NavLink to="/wishlist" className="relative text-gray-300 hover:text-white transition-colors duration-300 p-2">
             <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
            {wishlist.length > 0 && (
                <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-yellow-500 text-xs font-bold text-black">{wishlist.length}</span>
            )}
          </NavLink>
           <NavLink to="/cart" className="relative text-gray-300 hover:text-white transition-colors duration-300 p-2">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            {totalCartItems > 0 && (
                <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center justify-center rounded-full bg-yellow-500 text-xs font-bold text-black">{totalCartItems}</span>
            )}
          </NavLink>
          {currentUser ? (
            <div className="relative" ref={dropdownRef}>
              <button onClick={() => setDropdownOpen(!isDropdownOpen)} className="flex items-center space-x-3 rounded-full hover:bg-gray-800 p-1 transition-colors">
                <img src={currentUser.profilePicture} alt="Profile" className="w-8 h-8 rounded-full object-cover border-2 border-yellow-500/50" />
                <span className="text-white font-medium text-sm hidden sm:block">{currentUser.username}</span>
                <svg className={`w-4 h-4 text-gray-400 transition-transform hidden sm:block ${isDropdownOpen ? 'transform rotate-180' : ''}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
              {isDropdownOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-[#2a2a2a] rounded-md shadow-lg py-1 z-50 ring-1 ring-black ring-opacity-5">
                  <button onClick={handleLogout} className="flex items-center w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-gray-700 hover:text-white transition-colors">
                     <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clipRule="evenodd" />
                    </svg>
                    Sign Out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <button 
              onClick={() => toggleAuthModal(true)}
              className="border border-yellow-500 text-yellow-500 px-4 py-2 rounded-full text-sm font-semibold hover:bg-yellow-500 hover:text-black transition-all duration-300 whitespace-nowrap"
            >
              Sign In / Sign Up
            </button>
          )}
        </div>
      </nav>
    </header>
  );
};

export default Header;