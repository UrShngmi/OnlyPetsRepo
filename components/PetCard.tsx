import React from 'react';
import { Link } from 'react-router-dom';
import { Pet } from '../types';
import { useAppContext } from '../contexts/AppContext';

interface PetCardProps {
  pet: Pet;
}

const PetCard: React.FC<PetCardProps> = ({ pet }) => {
  const { wishlist, toggleWishlist, addToast } = useAppContext();
  const isInWishlist = wishlist.some(item => item.id === pet.id);

  const handleWishlistClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    toggleWishlist(pet);
    addToast(isInWishlist ? `${pet.name} removed from wishlist.` : `${pet.name} added to wishlist!`, 'success');
  };

  return (
    <div className="bg-[#2a2a2a] rounded-2xl overflow-hidden transform hover:scale-105 hover:shadow-2xl hover:shadow-yellow-500/10 transition-all duration-300 h-full flex flex-col group relative">
      <button 
        onClick={handleWishlistClick}
        className="absolute top-3 right-3 z-10 p-2 rounded-full bg-black bg-opacity-40 text-white hover:bg-opacity-60 transition-all"
        aria-label={isInWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" viewBox="0 0 20 20" fill={isInWishlist ? '#f59e0b' : 'currentColor'}>
          <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
        </svg>
      </button>
      <Link to={`/adoption/${pet.id}`} className="block h-full flex flex-col">
        <img
          className="w-full h-56 object-cover"
          src={pet.imageUrls[0]}
          alt={pet.name}
          loading="lazy"
        />
        <div className="p-5 flex-grow flex flex-col">
          <h3 className="text-xl font-bold text-white truncate">{pet.name}</h3>
          <p className="text-sm text-gray-400">{pet.breed}</p>
          <div className="mt-auto pt-4">
              <span className="inline-block bg-yellow-500 bg-opacity-20 text-yellow-400 text-xs font-semibold px-3 py-1 rounded-full">
                  View Details
              </span>
          </div>
        </div>
      </Link>
    </div>
  );
};

export default PetCard;