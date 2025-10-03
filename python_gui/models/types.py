"""
Data models for OnlyPets application
"""
from dataclasses import dataclass, field
from typing import List, Optional, Literal

@dataclass
class Pet:
    id: str
    name: str
    species: Literal['Dog', 'Cat', 'Bird', 'Other']
    breed: str
    age: int
    description: str
    quick_facts: List[str]
    image_urls: List[str]

@dataclass
class Service:
    id: str
    name: str
    description: str
    price: float
    image_url: str
    duration: int  # in minutes
    activities: List[str]
    notes: Optional[str] = None

@dataclass
class Product:
    id: str
    name: str
    price: float
    image: str

@dataclass
class CartItem:
    id: str
    name: str
    price: float
    image: str
    quantity: int

@dataclass
class Booking:
    service_id: str
    date: str  # YYYY-MM-DD
    time_slot: Literal['morning', 'afternoon']
    id: str = ""
    user_id: str = ""
    status: str = "confirmed"  # confirmed, cancelled

@dataclass
class User:
    id: str
    email: str
    username: str
    profile_picture: str  # path to image file
    password: str = ""  # In real app, this would be hashed

ToastType = Literal['success', 'error', 'info']

@dataclass
class Toast:
    id: int
    message: str
    type: ToastType
