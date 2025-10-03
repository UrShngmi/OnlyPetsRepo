export interface Pet {
  id: string;
  name: string;
  species: 'Dog' | 'Cat' | 'Bird' | 'Other';
  breed: string;
  age: number;
  description: string;
  quickFacts: string[];
  imageUrls: string[];
}

export interface Service {
  id:string;
  name: string;
  description: string;
  price: number;
  imageUrl: string;
  duration: number; // Duration in minutes
  activities: string[];
  notes?: string;
}

export interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
}

export interface CartItem extends Product {
  quantity: number;
}

export interface Booking {
  serviceId: string;
  date: string; // YYYY-MM-DD
  timeSlot: 'morning' | 'afternoon';
}

export type WishlistItem = Pet | Service;

export type ToastType = 'success' | 'error' | 'info';

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

export interface User {
  id: string;
  email: string;
  username: string;
  profilePicture: string; // base64 string or URL
}