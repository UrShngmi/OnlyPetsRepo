import React from 'react';
import { Link } from 'react-router-dom';
import { useAppContext } from '../contexts/AppContext';
import PetCard from '../components/PetCard';

const HomePage: React.FC = () => {
  const { pets, loading } = useAppContext();
  const featuredPets = pets.slice(0, 4);

  return (
    <div className="space-y-24">
      {/* Hero Section */}
      <div className="relative text-center md:text-left h-[70vh] flex items-center justify-center md:justify-start overflow-hidden rounded-3xl">
        <div 
          className="absolute inset-0 bg-cover bg-center z-0 transition-transform duration-500 hover:scale-105" 
          style={{ backgroundImage: 'url(https://picsum.photos/seed/happy-pet-owner/1600/900)', filter: 'brightness(0.5)' }}
        ></div>
        <div className="absolute inset-0 bg-gradient-to-r from-black via-black/70 to-transparent z-10"></div>
        
        <div className="relative z-20 p-8 md:p-16 max-w-2xl">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-4 leading-tight">
            Find Your <br/> Forever Friend
          </h1>
          <p className="text-lg md:text-xl text-gray-300 mb-8">
            At OnlyPets, we connect loving families with pets in need of a home. Explore our services and find the perfect companion today.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link 
              to="/adoption"
              className="inline-block bg-yellow-500 text-black font-bold py-3 px-8 rounded-full hover:bg-yellow-400 transition-all duration-300 text-lg"
            >
              Meet The Pets
            </Link>
            <Link 
              to="/services"
              className="inline-block bg-transparent border-2 border-gray-400 text-gray-200 font-bold py-3 px-8 rounded-full hover:bg-gray-400 hover:text-black transition-all duration-300 text-lg"
            >
              Our Services
            </Link>
          </div>
        </div>
      </div>

      {/* Why Choose Us Section */}
      <div className="text-center">
        <h2 className="text-4xl font-bold mb-4">Why Choose OnlyPets?</h2>
        <p className="text-lg text-gray-400 max-w-3xl mx-auto mb-12">We provide a seamless experience for adoption, top-tier pet services, and a community that cares.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-[#2a2a2a] p-8 rounded-2xl">
                <h3 className="text-2xl font-bold text-yellow-400 mb-3">Find a Friend</h3>
                <p className="text-gray-300">Browse our diverse selection of lovable pets waiting for a forever home.</p>
            </div>
            <div className="bg-[#2a2a2a] p-8 rounded-2xl">
                <h3 className="text-2xl font-bold text-yellow-400 mb-3">Expert Care</h3>
                <p className="text-gray-300">From grooming to health checkups, our professional services ensure your pet is happy and healthy.</p>
            </div>
            <div className="bg-[#2a2a2a] p-8 rounded-2xl">
                <h3 className="text-2xl font-bold text-yellow-400 mb-3">Quality Products</h3>
                <p className="text-gray-300">Shop a curated selection of the best food, toys, and accessories for your companion.</p>
            </div>
        </div>
      </div>

      {/* Featured Pets Section */}
      {!loading && featuredPets.length > 0 && (
        <div>
          <h2 className="text-4xl font-bold text-center mb-12">Featured Pets</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {featuredPets.map(pet => <PetCard key={pet.id} pet={pet} />)}
          </div>
        </div>
      )}

      {/* Testimonials */}
      <div>
        <h2 className="text-4xl font-bold text-center mb-12">What Our Friends Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-[#2a2a2a] p-8 rounded-2xl">
                <p className="text-gray-300 italic mb-4">"Adopting Buddy from OnlyPets was the best decision we've ever made. The process was so smooth and the staff were incredibly supportive. Our home feels complete now!"</p>
                <p className="font-bold text-yellow-400">- The Johnson Family</p>
            </div>
            <div className="bg-[#2a2a2a] p-8 rounded-2xl">
                <p className="text-gray-300 italic mb-4">"I use their grooming service every month for my poodle, Luna. They do an amazing job every time, and Luna always comes back happy and looking fabulous. Highly recommend!"</p>
                <p className="font-bold text-yellow-400">- Sarah L.</p>
            </div>
        </div>
      </div>

    </div>
  );
};

export default HomePage;
