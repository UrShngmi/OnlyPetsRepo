import React, { useState, useMemo } from 'react';
import { Pet } from '../types';
import PetCard from '../components/PetCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { useAppContext } from '../contexts/AppContext';

type SpeciesFilter = 'All' | 'Dog' | 'Cat' | 'Bird' | 'Other';

const AdoptionPage: React.FC = () => {
  const { pets, loading, error } = useAppContext();
  const [filter, setFilter] = useState<SpeciesFilter>('All');
  const [searchQuery, setSearchQuery] = useState('');

  const filteredPets = useMemo(() => {
    let result = pets;

    if (filter !== 'All') {
      result = result.filter(pet => pet.species === filter);
    }

    if (searchQuery) {
      const lowercasedQuery = searchQuery.toLowerCase().trim();
      if (lowercasedQuery) {
        result = result.filter(pet => 
          pet.name.toLowerCase().includes(lowercasedQuery) ||
          pet.species.toLowerCase().includes(lowercasedQuery) ||
          pet.breed.toLowerCase().includes(lowercasedQuery)
        );
      }
    }

    return result;
  }, [pets, filter, searchQuery]);

  const FilterButton: React.FC<{ species: SpeciesFilter }> = ({ species }) => (
    <button
      onClick={() => setFilter(species)}
      className={`px-6 py-2 rounded-full font-semibold transition-all duration-300 ${
        filter === species
          ? 'bg-yellow-500 text-black shadow-lg shadow-yellow-500/20'
          : 'bg-[#2a2a2a] text-gray-300 hover:bg-gray-700'
      }`}
    >
      {species}
    </button>
  );

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">MAKE A FRIEND</h1>
        <p className="text-lg text-gray-400">Select a pet</p>
      </div>

      <div className="max-w-md mx-auto mb-10">
        <div className="relative">
          <span className="absolute inset-y-0 left-0 flex items-center pl-4">
            <svg className="h-5 w-5 text-gray-500" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd" />
            </svg>
          </span>
          <input
            type="text"
            placeholder="Search by name, species, or breed..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-[#2a2a2a] text-white p-3 pl-11 rounded-full border border-gray-700 focus:outline-none focus:ring-2 focus:ring-yellow-500 transition-colors"
          />
        </div>
      </div>

      <div className="flex justify-center space-x-2 md:space-x-4 mb-10">
        <FilterButton species="All" />
        <FilterButton species="Dog" />
        <FilterButton species="Cat" />
        <FilterButton species="Bird" />
        <FilterButton species="Other" />
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : error ? (
        <div className="text-center py-10 px-4 bg-red-900 bg-opacity-30 rounded-lg">
            <p className="text-red-400">{error}</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-8">
            {filteredPets.map(pet => (
              <PetCard key={pet.id} pet={pet} />
            ))}
          </div>
          {filteredPets.length === 0 && !loading && (
             <div className="text-center py-16 bg-[#2a2a2a] rounded-2xl mt-8">
                <h2 className="text-2xl font-semibold text-white mb-4">No Pets Found</h2>
                <p className="text-gray-400">Try adjusting your search or filters.</p>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default AdoptionPage;