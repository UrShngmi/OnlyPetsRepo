import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Pet, Service, WishlistItem, Toast, ToastType, Product, CartItem, Booking, User } from '../types';
import { generatePetsData } from '../services/geminiService';
import { getPetImages, getServiceImage } from '../utils/imageUtils';

interface AppContextType {
  pets: Pet[];
  services: Service[];
  wishlist: WishlistItem[];
  cart: CartItem[];
  bookings: Booking[];
  isAuthModalOpen: boolean;
  isProfileModalOpen: boolean;
  toasts: Toast[];
  loading: boolean;
  error: string | null;
  currentUser: User | null;
  toggleWishlist: (item: WishlistItem) => void;
  toggleAuthModal: (isOpen: boolean) => void;
  toggleProfileModal: (isOpen: boolean) => void;
  addToast: (message: string, type?: ToastType) => void;
  removeToast: (id: number) => void;
  addToCart: (product: Product) => void;
  removeFromCart: (productId: string) => void;
  updateCartQuantity: (productId: string, newQuantity: number) => void;
  clearCart: () => void;
  addBooking: (booking: Booking) => void;
  signup: (email: string, pass: string) => Promise<boolean>;
  login: (email: string, pass: string) => Promise<boolean>;
  socialLogin: (provider: 'google' | 'facebook') => void;
  logout: () => void;
  updateUserProfile: (userId: string, updates: { username?: string; profilePicture?: string; }) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const defaultUserProfilePic = "data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%239ca3af'%3e%3cpath fill-rule='evenodd' d='M18.685 19.097A9.723 9.723 0 0021.75 12c0-5.385-4.365-9.75-9.75-9.75S2.25 6.615 2.25 12a9.723 9.723 0 003.065 7.097A9.716 9.716 0 0012 21.75a9.716 9.716 0 006.685-2.653zm-12.54-1.285A7.486 7.486 0 0112 15a7.486 7.486 0 015.855 2.812A8.224 8.224 0 0112 20.25a8.224 8.224 0 01-5.855-2.438zM15.75 9a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z' clip-rule='evenodd' /%3e%3c/svg%3e";

export const AppProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [pets, setPets] = useState<Pet[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [isAuthModalOpen, setAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setProfileModalOpen] = useState(false);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);

        const storedUser = localStorage.getItem('currentUser');
        if (storedUser) {
            setCurrentUser(JSON.parse(storedUser));
        }

        const petsData = await generatePetsData();

        if (petsData.length === 0) {
            setError('Could not fetch pet data. Please check if your API key is configured correctly.');
        }

        const petsWithImages: Pet[] = petsData.map(p => ({
            ...p,
            imageUrls: getPetImages(p),
        }));
        setPets(petsWithImages);
        
        const servicesData: Omit<Service, 'imageUrl'>[] = [
          { id: 'service_01', name: 'Full Grooming Package', description: 'A complete pampering session for your pet.', price: 1500.00, duration: 120, activities: ['Warm bath', 'Haircut', 'Nail trim'] },
          { id: 'service_02', name: 'Annual Health Checkup', description: 'A comprehensive veterinary examination.', price: 2500.00, duration: 45, activities: ['Physical exam', 'Vaccinations', 'Parasite check'] },
          { id: 'service_03', name: 'Basic Obedience Training', description: 'A 4-week group course for essential commands.', price: 8000.00, duration: 60, activities: ['Sit, stay, come', 'Leash manners', 'Socialization'] },
          { id: 'service_04', name: 'Pet Sitting (Per Day)', description: 'Peace of mind while you\'re away.', price: 1000.00, duration: 1440, activities: ['Two walks', 'Playtime', 'Feeding'] },
          { id: 'service_05', name: 'Dog Walking (30 min)', description: 'A refreshing 30-minute walk for your dog.', price: 500.00, duration: 30, activities: ['30-min walk', 'Water break', 'Paw wipe-down'] }
        ];

        const detailedServices: Service[] = servicesData.map(service => ({
            ...service,
            imageUrl: getServiceImage(service),
        }));
        setServices(detailedServices);
        
        const today = new Date();
        const conflictDate = new Date(today.setDate(today.getDate() + 5)).toISOString().split('T')[0];
        setBookings([{ serviceId: 'service_01', date: conflictDate, timeSlot: 'morning' }]);

      } catch (err) {
        setError('An error occurred while fetching initial data.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const signup = async (email: string, pass: string): Promise<boolean> => {
    const users: User[] = JSON.parse(localStorage.getItem('users') || '[]');
    if (users.find(u => u.email === email)) {
      addToast('An account with this email already exists.', 'error');
      return false;
    }

    const newUser: User = {
      id: Date.now().toString(),
      email,
      username: email.split('@')[0], // Default username
      profilePicture: defaultUserProfilePic,
    };

    // In a real app, you would hash the password 'pass'
    users.push(newUser);
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('currentUser', JSON.stringify(newUser));
    setCurrentUser(newUser);
    toggleAuthModal(false);
    toggleProfileModal(true); // Open profile setup after signup
    return true;
  };

  const login = async (email: string, pass: string): Promise<boolean> => {
    const users: User[] = JSON.parse(localStorage.getItem('users') || '[]');
    const user = users.find(u => u.email === email);

    // In a real app, you would compare a hashed password
    if (user) {
      localStorage.setItem('currentUser', JSON.stringify(user));
      setCurrentUser(user);
      toggleAuthModal(false);
      addToast(`Welcome back, ${user.username}!`, 'success');
      return true;
    } else {
      addToast('Invalid email or password.', 'error');
      return false;
    }
  };

  const socialLogin = (provider: 'google' | 'facebook') => {
    // This simulates fetching data from a social provider.
    const mockSocialData = {
        google: {
            email: `jane.doe.${Math.floor(Math.random() * 10000)}@google.com`,
            username: 'Jane Doe',
            profilePicture: `https://picsum.photos/seed/janedoe/200`
        },
        facebook: {
            email: `john.smith.${Math.floor(Math.random() * 10000)}@facebook.com`,
            username: 'John Smith',
            profilePicture: `https://picsum.photos/seed/johnsmith/200`
        }
    };

    const socialData = mockSocialData[provider];
    const users: User[] = JSON.parse(localStorage.getItem('users') || '[]');
    
    // In this simulation, we check if any user from this provider exists.
    // A real app would use a unique social ID.
    let user = users.find(u => u.email.includes(`@${provider}.com`));
    
    if (user) {
        // If a user from this provider exists, log them in.
        localStorage.setItem('currentUser', JSON.stringify(user));
        setCurrentUser(user);
        toggleAuthModal(false);
        addToast(`Welcome back, ${user.username}!`, 'success');
    } else {
        // Otherwise, create a new user with the simulated social data.
        const newUser: User = {
            id: Date.now().toString(),
            email: socialData.email,
            username: socialData.username,
            profilePicture: socialData.profilePicture,
        };
        users.push(newUser);
        localStorage.setItem('users', JSON.stringify(users));
        localStorage.setItem('currentUser', JSON.stringify(newUser));
        setCurrentUser(newUser);
        toggleAuthModal(false);
        toggleProfileModal(true); // Open profile setup, which will be pre-populated.
        addToast('Account created successfully! Please review your profile.', 'success');
    }
  };

  const logout = () => {
    localStorage.removeItem('currentUser');
    setCurrentUser(null);
    addToast('You have been signed out.', 'info');
  };
  
  const updateUserProfile = (userId: string, updates: { username?: string; profilePicture?: string; }) => {
    const users: User[] = JSON.parse(localStorage.getItem('users') || '[]');
    const userIndex = users.findIndex(u => u.id === userId);

    if (userIndex !== -1) {
        const updatedUser = { ...users[userIndex], ...updates };
        users[userIndex] = updatedUser;

        localStorage.setItem('users', JSON.stringify(users));
        localStorage.setItem('currentUser', JSON.stringify(updatedUser));
        setCurrentUser(updatedUser);
        addToast('Profile updated successfully!', 'success');
    }
  };

  const toggleWishlist = (item: WishlistItem) => {
    setWishlist(prev => {
      const exists = prev.find(i => i.id === item.id);
      if (exists) {
        return prev.filter(i => i.id !== item.id);
      }
      return [...prev, item];
    });
  };

  const toggleAuthModal = (isOpen: boolean) => setAuthModalOpen(isOpen);
  const toggleProfileModal = (isOpen: boolean) => setProfileModalOpen(isOpen);
  
  const addToast = (message: string, type: ToastType = 'info') => {
    const id = Date.now();
    setToasts(prev => [...prev, { id, message, type }]);
  };

  const removeToast = (id: number) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const addToCart = (product: Product) => {
    setCart(prevCart => {
      const existingItem = prevCart.find(item => item.id === product.id);
      if (existingItem) {
        return prevCart.map(item =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  const removeFromCart = (productId: string) => {
    setCart(prevCart => prevCart.filter(item => item.id !== productId));
  };

  const updateCartQuantity = (productId: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeFromCart(productId);
    } else {
      setCart(prevCart =>
        prevCart.map(item =>
          item.id === productId ? { ...item, quantity: newQuantity } : item
        )
      );
    }
  };
  
  const clearCart = () => setCart([]);

  const addBooking = (newBooking: Booking) => {
    setBookings(prev => [...prev, newBooking]);
  };

  return (
    <AppContext.Provider value={{
      pets,
      services,
      wishlist,
      cart,
      bookings,
      isAuthModalOpen,
      isProfileModalOpen,
      toasts,
      loading,
      error,
      currentUser,
      toggleWishlist,
      toggleAuthModal,
      toggleProfileModal,
      addToast,
      removeToast,
      addToCart,
      removeFromCart,
      updateCartQuantity,
      clearCart,
      addBooking,
      signup,
      login,
      socialLogin,
      logout,
      updateUserProfile
    }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useAppContext must be used within an AppProvider');
  }
  return context;
};