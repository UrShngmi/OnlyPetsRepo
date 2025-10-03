import React from 'react';
import ServiceCard from '../components/ServiceCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { useAppContext } from '../contexts/AppContext';

const ServicesPage: React.FC = () => {
  const { services, loading, error } = useAppContext();

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-5xl font-bold mb-2">Our Services</h1>
        <p className="text-lg text-gray-400">Professional care for your beloved pets</p>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : error ? (
         <div className="text-center py-10 px-4 bg-red-900 bg-opacity-30 rounded-lg">
            <p className="text-red-400">{error}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 items-start">
          {services.map(service => (
            <ServiceCard key={service.id} service={service} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ServicesPage;