import React, { useState } from 'react';
import { useAppContext } from '../contexts/AppContext';

type AuthMode = 'login' | 'signup';

const AuthModal: React.FC = () => {
  const { isAuthModalOpen, toggleAuthModal, addToast, login, signup, socialLogin } = useAppContext();
  const [mode, setMode] = useState<AuthMode>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState(''); // Only for signup

  if (!isAuthModalOpen) {
    return null;
  }
  
  const clearForm = () => {
    setEmail('');
    setPassword('');
    setFullName('');
  };
  
  const handleClose = () => {
    toggleAuthModal(false);
    clearForm();
  };
  
  const switchMode = (newMode: AuthMode) => {
    setMode(newMode);
    clearForm();
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await login(email, password);
    if (success) {
      clearForm();
    }
  }

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await signup(email, password);
    if (success) {
      addToast('Signup successful! Welcome!', 'success');
      clearForm();
    }
  }
  
  const handleSocialLogin = (provider: 'google' | 'facebook') => {
    socialLogin(provider);
  }

  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 transition-opacity duration-300"
      onClick={handleClose}
    >
      <div 
        className="bg-[#2a2a2a] rounded-2xl shadow-2xl shadow-yellow-500/10 w-full max-w-md p-8 transform transition-all duration-300 scale-95"
        onClick={e => e.stopPropagation()}
        style={{ animation: 'fade-in 0.3s ease-out forwards' }}
      >
        <div className="flex mb-6 border-b border-gray-700">
          <button 
            onClick={() => switchMode('login')}
            className={`w-1/2 py-3 text-lg font-semibold transition-colors duration-300 ${mode === 'login' ? 'text-yellow-400 border-b-2 border-yellow-400' : 'text-gray-400'}`}
          >
            Login
          </button>
          <button 
            onClick={() => switchMode('signup')}
            className={`w-1/2 py-3 text-lg font-semibold transition-colors duration-300 ${mode === 'signup' ? 'text-yellow-400 border-b-2 border-yellow-400' : 'text-gray-400'}`}
          >
            Sign Up
          </button>
        </div>
        
        <div className="space-y-4">
             <button onClick={() => handleSocialLogin('google')} className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-white text-gray-800 rounded-lg font-semibold hover:bg-gray-200 transition-colors">
                 <svg className="w-6 h-6" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                 Sign in with Google
             </button>
              <button onClick={() => handleSocialLogin('facebook')} className="w-full flex items-center justify-center gap-3 py-3 px-4 bg-[#1877F2] text-white rounded-lg font-semibold hover:bg-[#166eab] transition-colors">
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M22 12c0-5.52-4.48-10-10-10S2 6.48 2 12c0 4.84 3.44 8.87 8 9.8V15H8v-3h2V9.5C10 7.57 11.57 6 13.5 6H16v3h-2c-.55 0-1 .45-1 1v2h3l-.5 3h-2.5v6.8c4.56-.93 8-4.96 8-9.8z"/>
                </svg>
                Continue with Facebook
            </button>
        </div>

        <div className="my-6 flex items-center">
            <div className="flex-grow border-t border-gray-600"></div>
            <span className="mx-4 text-gray-500 text-sm">OR</span>
            <div className="flex-grow border-t border-gray-600"></div>
        </div>

        {mode === 'login' ? (
          <form onSubmit={handleLogin}>
            <div className="space-y-4">
              <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
            </div>
            <button type="submit" className="w-full mt-6 bg-yellow-500 text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition-colors duration-300">
              Login
            </button>
          </form>
        ) : (
          <form onSubmit={handleSignup}>
            <div className="space-y-4">
              <input type="text" placeholder="Full Name" value={fullName} onChange={e => setFullName(e.target.value)} className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
              <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
              <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} className="w-full bg-[#1c1c1c] text-white p-3 rounded-lg border border-gray-600 focus:outline-none focus:ring-2 focus:ring-yellow-500" required />
            </div>
            <button type="submit" className="w-full mt-6 bg-yellow-500 text-black font-bold py-3 rounded-lg hover:bg-yellow-400 transition-colors duration-300">
              Create Account
            </button>
          </form>
        )}
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

export default AuthModal;