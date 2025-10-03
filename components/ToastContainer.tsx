import React from 'react';
import { useAppContext } from '../contexts/AppContext';
import Toast from './Toast';

const ToastContainer: React.FC = () => {
  const { toasts } = useAppContext();

  return (
    <div className="fixed top-24 right-5 z-50 space-y-3">
      {toasts.map(toast => (
        <Toast key={toast.id} toast={toast} />
      ))}
    </div>
  );
};

export default ToastContainer;
