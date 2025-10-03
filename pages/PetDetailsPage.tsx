import React, { useState, useEffect, useMemo } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Pet } from '../types';
import LoadingSpinner from '../components/LoadingSpinner';
import { useAppContext } from '../contexts/AppContext';

const PetDetailsPage: React.FC = () => {
  const { petId } = useParams<{ petId: string }>();
  const navigate = useNavigate();
  const { pets, loading, error: contextError } = useAppContext();
  const [activeImageIndex, setActiveImageIndex] = useState(0);

  const pet = useMemo(() => pets.find(p => p.id === petId), [pets, petId]);

  useEffect(() => {
    // If data has loaded and no pet was found, navigate away.
    if (!loading && !pet && petId) {
        setTimeout(() => navigate('/adoption'), 100);
    }
  }, [loading, pet, petId, navigate]);

  if (loading) return <LoadingSpinner />;
  if (contextError) return <div className="text-center text-red-500 text-xl">{contextError}</div>;
  if (!pet) return null; // Render nothing while redirecting

  const { name, breed, description, quickFacts, age, imageUrls } = pet;

  return (
    <div className="bg-[#121212] p-8 md:p-12 rounded-3xl">
        <div className="text-left mb-12">
            <h1 className="text-4xl font-bold tracking-wider text-gray-300">ABOUT {name.toUpperCase()}</h1>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start">
            <div className="relative aspect-square w-full flex items-center justify-center">
                {imageUrls.map((url, index) => (
                    <img
                        key={index}
                        src={url}
                        alt={`${name} - view ${index + 1}`}
                        onClick={() => setActiveImageIndex(index)}
                        className={`absolute w-[85%] h-[85%] object-cover rounded-3xl shadow-2xl shadow-black transition-all duration-500 ease-in-out cursor-pointer hover:scale-105`}
                        style={{
                            transform: `rotate(${ (index - activeImageIndex) * 5}deg) translateX(${ (index - activeImageIndex) * 10}%) scale(${1 - Math.abs(index - activeImageIndex) * 0.1})`,
                            zIndex: imageUrls.length - Math.abs(index - activeImageIndex),
                            filter: index === activeImageIndex ? 'brightness(1)' : 'brightness(0.6)',
                        }}
                    />
                ))}
            </div>
            <div className="flex flex-col h-full">
                <h2 className="text-5xl lg:text-7xl font-extrabold text-white">{name.toUpperCase()}</h2>
                <p className="text-xl lg:text-2xl text-gray-400 mb-6">{breed}</p>
                 <p className="text-lg text-yellow-400 mb-4">{age} year{age > 1 ? 's' : ''} old</p>
                <p className="text-gray-300 leading-relaxed mb-6">
                    {description}
                </p>
                <div className="space-y-2 mb-8">
                    {quickFacts.map((fact, index) => (
                         <p key={index} className="text-gray-400 flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-3 text-yellow-500 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                            </svg>
                            {fact}
                         </p>
                    ))}
                </div>
                <div className="mt-auto">
                    <Link
                        to={`/booking/pet/${pet.id}`}
                        className="w-full text-center md:w-auto bg-yellow-500 text-black font-bold py-4 px-12 rounded-lg hover:bg-yellow-400 transition-all duration-300 text-lg transform hover:scale-105 inline-block"
                    >
                        ADOPT
                    </Link>
                </div>
            </div>
        </div>
    </div>
  );
};

export default PetDetailsPage;
