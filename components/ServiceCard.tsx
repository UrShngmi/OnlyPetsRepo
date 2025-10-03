import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Service } from '../types';

interface ServiceCardProps {
  service: Service;
}

const ServiceCard: React.FC<ServiceCardProps> = ({ service }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-[#2a2a2a] rounded-2xl overflow-hidden shadow-lg flex flex-col relative group">
       <div 
        className="absolute inset-0 bg-cover bg-center z-0 transition-transform duration-500 group-hover:scale-110" 
        style={{ backgroundImage: `url(${service.imageUrl})` }}
      ></div>
      <div className="absolute inset-0 bg-black bg-opacity-60 group-hover:bg-opacity-75 transition-all duration-300 z-10"></div>
      
      <div className="p-6 flex-grow flex flex-col justify-between z-20">
        <div>
            <h3 className="text-2xl font-bold text-white mb-2">{service.name}</h3>
            <p className="text-yellow-400 text-sm mb-2">{service.duration > 60 ? `${service.duration / 60} hours` : `${service.duration} minutes`}</p>
            <p className="text-gray-300 text-sm mb-4">{service.description}</p>
            
            <div className={`space-y-1 mb-4 overflow-hidden transition-all duration-500 ease-in-out`} style={{ maxHeight: isExpanded ? '500px' : '60px' }}>
              {service.activities.map((activity, index) => (
                <p key={index} className="text-xs text-gray-400 flex items-start">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2 mt-0.5 text-yellow-500 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span>{activity}</span>
                </p>
              ))}
            </div>
            
            {service.activities.length > 2 && (
              <button onClick={() => setIsExpanded(!isExpanded)} className="text-xs text-yellow-500 hover:text-yellow-400 font-semibold pl-6 mb-4">
                {isExpanded ? 'Show less' : '...and more'}
              </button>
            )}
        </div>
        <div className="flex justify-between items-center mt-auto pt-4 border-t border-gray-700/50">
          <p className="text-xl font-semibold text-yellow-400">₱{service.price.toFixed(2)}</p>
          <Link 
            to={`/booking/service/${service.id}`}
            className="bg-yellow-500 text-black font-bold py-2 px-4 rounded-lg hover:bg-yellow-400 transition-colors duration-300 transform group-hover:scale-105"
          >
            Book Now
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ServiceCard;