import React, { useEffect } from 'react';
import { Toast as ToastType } from '../types';
import { useAppContext } from '../contexts/AppContext';

interface ToastProps {
  toast: ToastType;
}

const Toast: React.FC<ToastProps> = ({ toast }) => {
  const { removeToast } = useAppContext();

  useEffect(() => {
    const timer = setTimeout(() => {
      removeToast(toast.id);
    }, 3000);

    return () => {
      clearTimeout(timer);
    };
  }, [toast.id, removeToast]);

  const typeClasses = {
    success: 'bg-green-600/80 border-green-500',
    error: 'bg-red-600/80 border-red-500',
    info: 'bg-blue-600/80 border-blue-500',
  };

  return (
    <div 
      className={`flex items-center text-white px-6 py-3 rounded-lg shadow-lg border-l-4 backdrop-blur-sm ${typeClasses[toast.type]} animate-slide-in-right`}
    >
      <div className="flex-1">
        <p className="font-semibold">{toast.message}</p>
      </div>
      <button onClick={() => removeToast(toast.id)} className="ml-4 text-xl font-semibold">&times;</button>
      <style>{`
        @keyframes slide-in-right {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        .animate-slide-in-right {
            animation: slide-in-right 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
        }
      `}</style>
    </div>
  );
};

export default Toast;
