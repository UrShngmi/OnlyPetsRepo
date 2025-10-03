import React, { useState, useEffect, useRef } from 'react';
import { useAppContext } from '../contexts/AppContext';

const ProfileSetupModal: React.FC = () => {
  const { isProfileModalOpen, toggleProfileModal, currentUser, updateUserProfile } = useAppContext();
  const [username, setUsername] = useState('');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (currentUser) {
      setUsername(currentUser.username);
      setImagePreview(currentUser.profilePicture);
    }
  }, [currentUser, isProfileModalOpen]);

  if (!isProfileModalOpen || !currentUser) {
    return null;
  }

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSave = () => {
    updateUserProfile(currentUser.id, {
        username: username || currentUser.username,
        profilePicture: imagePreview || currentUser.profilePicture,
    });
    toggleProfileModal(false);
  };

  const handleSkip = () => {
    toggleProfileModal(false);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 transition-opacity duration-300">
      <div 
        className="bg-[#2a2a2a] rounded-2xl shadow-2xl shadow-yellow-500/10 w-full max-w-md p-8 transform transition-all duration-300 scale-95"
        style={{ animation: 'fade-in 0.3s ease-out forwards' }}
      >
        <h2 className="text-2xl font-bold text-white mb-4 text-center">Set Up Your Profile</h2>
        <p className="text-center text-gray-400 mb-6">Welcome! Personalize your account.</p>
        
        <div className="flex flex-col items-center space-y-4">
            <div className="relative">
                <img 
                    src={imagePreview || ''} 
                    alt="Profile Preview" 
                    className="w-24 h-24 rounded-full object-cover border-2 border-gray-600"
                />
                <button 
                    onClick={() => fileInputRef.current?.click()}
                    className="absolute bottom-0 right-0 bg-yellow-500 text-black w-8 h-8 rounded-full flex items-center justify-center hover:bg-yellow-400 transition-colors"
                    aria-label="Upload profile picture"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                    </svg>
                </button>
            </div>
            <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept="image/*"
                onChange={handleImageChange}
            />
            <input 
                type="text" 
                placeholder="Enter your display name" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 text-center" 
                required 
            />
        </div>

        <div className="mt-8 grid grid-cols-2 gap-4">
            <button onClick={handleSkip} className="w-full bg-gray-600 text-white font-bold py-3 rounded-lg hover:bg-gray-500 transition-colors duration-300">
              Skip for Now
            </button>
            <button onClick={handleSave} className="w-full bg-yellow-500 text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition-colors duration-300">
              Save Profile
            </button>
        </div>
      </div>
      <style>{`
        @keyframes fade-in {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
      `}</style>
    </div>
  );
};

export default ProfileSetupModal;
