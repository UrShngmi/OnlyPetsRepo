import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import PetCard from '../components/PetCard';
import ServiceCard from '../components/ServiceCard';
import { Pet, Service } from '../types';
import { Link } from 'react-router-dom';

const WishlistPage: React.FC = () => {
  const { wishlist } = useAppContext();

  const pets = wishlist.filter(item => 'species' in item) as Pet[];
  const services = wishlist.filter(item => 'price' in item) as Service[];

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">Your Wishlist</h1>
        <p className="text-lg text-gray-400">Your favorite pets and services, all in one place.</p>
      </div>

      {wishlist.length === 0 ? (
        <div className="text-center py-16 bg-[#2a2a2a] rounded-2xl">
            <h2 className="text-2xl font-semibold text-white mb-4">Your wishlist is empty!</h2>
            <p className="text-gray-400 mb-6">Browse our pets and services to find your new best friend.</p>
            <Link 
                to="/adoption"
                className="inline-block bg-yellow-500 text-black font-bold py-3 px-8 rounded-lg hover:bg-yellow-400 transition-all"
            >
                Find Pets
            </Link>
        </div>
      ) : (
        <>
          {pets.length > 0 && (
            <div className="mb-12">
              <h2 className="text-3xl font-bold mb-6">Favorite Pets</h2>
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
                {pets.map(pet => <PetCard key={pet.id} pet={pet} />)}
              </div>
            </div>
          )}
          {services.length > 0 && (
            <div>
              <h2 className="text-3xl font-bold mb-6">Saved Services</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-start">
                {services.map(service => <ServiceCard key={service.id} service={service} />)}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default WishlistPage;