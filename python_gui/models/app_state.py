"""
Central application state manager
"""
import json
import os
from typing import List, Optional, Callable
from datetime import datetime, timedelta
from models.types import Pet, Service, Product, CartItem, Booking, User, Toast, ToastType

class AppState:
    def __init__(self):
        # Data
        self.pets: List[Pet] = []
        self.services: List[Service] = []
        self.wishlist: List[Pet | Service] = []
        self.cart: List[CartItem] = []
        self.bookings: List[Booking] = []
        
        # UI State
        self.toasts: List[Toast] = []
        self.loading: bool = False
        self.error: Optional[str] = None
        self.current_user: Optional[User] = None
        self.is_auth_modal_open: bool = False
        self.is_profile_modal_open: bool = False
        
        # Callbacks for UI updates
        self.on_state_change: Optional[Callable] = None
        
        # Data file paths
        self.data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(self.data_dir, exist_ok=True)
        self.users_file = os.path.join(self.data_dir, 'users.json')
        
        # Load initial data
        self._load_users()
        self._load_sample_data()
    
    def _load_users(self):
        """Load users from file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    users_data = json.load(f)
                    # Check for current user
                    for user_data in users_data:
                        if user_data.get('is_current'):
                            self.current_user = User(**{k: v for k, v in user_data.items() if k != 'is_current'})
                            break
            except Exception as e:
                print(f"Error loading users: {e}")
    
    def _save_users(self):
        """Save users to file"""
        try:
            users_data = []
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    users_data = json.load(f)
            
            # Update or add current user
            if self.current_user:
                user_dict = {
                    'id': self.current_user.id,
                    'email': self.current_user.email,
                    'username': self.current_user.username,
                    'profile_picture': self.current_user.profile_picture,
                    'password': self.current_user.password,
                    'is_current': True
                }
                
                # Remove is_current from all others
                for user in users_data:
                    user['is_current'] = False
                
                # Update or append
                existing = next((i for i, u in enumerate(users_data) if u['id'] == self.current_user.id), None)
                if existing is not None:
                    users_data[existing] = user_dict
                else:
                    users_data.append(user_dict)
            
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def _load_sample_data(self):
        """Load sample pets and services data"""
        # Sample pets - matching actual asset folder structure
        pets_data = [
            {"id": "pet_01", "name": "Buddy", "species": "Dog", "breed": "Golden Retriever", "age": 3, 
             "description": "Buddy is a friendly and energetic golden retriever who loves to play fetch and go on long walks. He's great with kids and other pets.", 
             "quick_facts": ["Loves water and swimming", "House trained", "Knows basic commands", "Great with children"]},
            {"id": "pet_02", "name": "Whiskers", "species": "Cat", "breed": "Siamese", "age": 2, 
             "description": "Whiskers is an elegant Siamese cat with piercing blue eyes. She's affectionate, vocal, and loves to be the center of attention.", 
             "quick_facts": ["Very talkative", "Enjoys lap time", "Indoor cat", "Playful and curious"]},
            {"id": "pet_03", "name": "Max", "species": "Dog", "breed": "German Shepherd", "age": 5, 
             "description": "Max is a loyal and intelligent German Shepherd. He's protective, well-trained, and perfect for active families.", 
             "quick_facts": ["Highly trainable", "Protective instinct", "Needs daily exercise", "Great guard dog"]},
            {"id": "pet_04", "name": "Luna", "species": "Cat", "breed": "Persian", "age": 1, 
             "description": "Luna is a beautiful Persian kitten with soft, fluffy fur. She's gentle, calm, and loves to be pampered.", 
             "quick_facts": ["Requires regular grooming", "Very calm", "Loves soft beds", "Indoor only"]},
            {"id": "pet_05", "name": "Charlie", "species": "Dog", "breed": "Beagle", "age": 4, 
             "description": "Charlie is a sweet beagle with a nose for adventure. He's friendly, loyal, and loves treats!", 
             "quick_facts": ["Good with other dogs", "Loves treats", "Enjoys walks", "Calm temperament"]},
            {"id": "pet_06", "name": "Mittens", "species": "Cat", "breed": "Tabby", "age": 4, 
             "description": "Mittens is a sweet tabby cat who loves cuddles and sunny windowsills. She's gentle and independent.", 
             "quick_facts": ["Independent", "Loves sun bathing", "Gentle nature", "Low maintenance"]},
            {"id": "pet_07", "name": "Rocky", "species": "Dog", "breed": "Bulldog", "age": 2, 
             "description": "Rocky is a charming English Bulldog with a lovable wrinkly face. He's calm, friendly, and great for apartment living.", 
             "quick_facts": ["Low energy", "Apartment friendly", "Loves naps", "Great companion"]},
            {"id": "pet_08", "name": "Tweety", "species": "Bird", "breed": "Canary", "age": 1, 
             "description": "Tweety is a cheerful canary with a beautiful singing voice. Perfect for bird lovers!", 
             "quick_facts": ["Beautiful singer", "Bright yellow color", "Easy to care for", "Social bird"]},
            {"id": "pet_09", "name": "Daisy", "species": "Dog", "breed": "Poodle", "age": 2, 
             "description": "Daisy is an intelligent toy poodle with a hypoallergenic coat. She's energetic, smart, and loves to learn tricks.", 
             "quick_facts": ["Hypoallergenic", "Highly intelligent", "Loves tricks", "Great for allergies"]},
            {"id": "pet_10", "name": "Shadow", "species": "Cat", "breed": "Black Cat", "age": 5, 
             "description": "Shadow is a mysterious black cat with golden eyes. He's affectionate, calm, and brings good luck!", 
             "quick_facts": ["Sleek black coat", "Very affectionate", "Calm demeanor", "Lucky charm"]},
            {"id": "pet_11", "name": "Coco", "species": "Bird", "breed": "Cockatiel", "age": 2, 
             "description": "Coco is a friendly cockatiel who loves to whistle and interact with people. She's social and entertaining.", 
             "quick_facts": ["Loves whistling", "Very social", "Hand-tamed", "Playful character"]},
            {"id": "pet_12", "name": "Bella", "species": "Cat", "breed": "Maine Coon", "age": 3, 
             "description": "Bella is a majestic Maine Coon with a playful personality. She's large, fluffy, and loves interactive toys.", 
             "quick_facts": ["Large breed", "Playful nature", "Good with children", "Dog-like personality"]}
        ]
        
        for pet_data in pets_data:
            # Map pet IDs to actual folder names
            pet_folder_map = {
                "pet_01": "pet_01_buddy",
                "pet_02": "pet_02_whiskers", 
                "pet_03": "pet_03_max",
                "pet_04": "pet_04_luna",
                "pet_05": "pet_05_charlie",
                "pet_06": "pet_06_mittens",
                "pet_07": "pet_07_rocky",
                "pet_08": "pet_08_tweety",
                "pet_09": "pet_09_daisy",
                "pet_10": "pet_10_shadow",
                "pet_11": "pet_11_coco",
                "pet_12": "pet_12_bella"
            }
            
            folder_name = pet_folder_map.get(pet_data['id'], pet_data['id'])
            pet_name = pet_data['name'].lower()
            
            # Create image URLs based on actual file structure
            image_urls = [
                f"assets/pets/{folder_name}/{pet_name}.png",
                f"assets/pets/{folder_name}/{pet_name}1.png", 
                f"assets/pets/{folder_name}/{pet_name}2.png",
                f"assets/pets/{folder_name}/{pet_name}3.png"
            ]
            
            pet = Pet(
                id=pet_data['id'],
                name=pet_data['name'],
                species=pet_data['species'],
                breed=pet_data['breed'],
                age=pet_data['age'],
                description=pet_data['description'],
                quick_facts=pet_data['quick_facts'],
                image_urls=image_urls
            )
            self.pets.append(pet)
        
        # Sample services - using actual asset files
        self.services = [
            Service(
                id='service_01',
                name='Full Grooming Package',
                description='A complete pampering session for your pet.',
                price=1500.00,
                duration=120,
                activities=['Warm bath', 'Haircut', 'Nail trim'],
                image_url='assets/services/grooming.png'
            ),
            Service(
                id='service_02',
                name='Annual Health Checkup',
                description='A comprehensive veterinary examination.',
                price=2500.00,
                duration=45,
                activities=['Physical exam', 'Vaccinations', 'Parasite check'],
                image_url='assets/services/checkup.png'
            ),
            Service(
                id='service_03',
                name='Basic Obedience Training',
                description='A 4-week group course for essential commands.',
                price=8000.00,
                duration=60,
                activities=['Sit, stay, come', 'Leash manners', 'Socialization'],
                image_url='assets/services/training.png'
            ),
            Service(
                id='service_04',
                name='Pet Sitting (Per Day)',
                description='Peace of mind while you\'re away.',
                price=1000.00,
                duration=1440,
                activities=['Two walks', 'Playtime', 'Feeding'],
                image_url='assets/services/sitting.png'
            ),
            Service(
                id='service_05',
                name='Dog Walking (30 min)',
                description='A refreshing 30-minute walk for your dog.',
                price=500.00,
                duration=30,
                activities=['30-min walk', 'Water break', 'Paw wipe-down'],
                image_url='assets/services/walking.png'
            )
        ]
        
        # Add a sample booking for conflict testing
        today = datetime.now()
        conflict_date = (today + timedelta(days=5)).strftime('%Y-%m-%d')
        self.bookings.append(Booking(service_id='service_01', date=conflict_date, time_slot='morning'))
    
    def notify_change(self):
        """Notify UI of state changes"""
        if self.on_state_change:
            self.on_state_change()
    
    # Toast methods
    def add_toast(self, message: str, toast_type: ToastType = 'info'):
        """Add a toast notification"""
        toast_id = int(datetime.now().timestamp() * 1000)
        self.toasts.append(Toast(id=toast_id, message=message, type=toast_type))
        self.notify_change()
    
    def remove_toast(self, toast_id: int):
        """Remove a toast notification"""
        self.toasts = [t for t in self.toasts if t.id != toast_id]
        self.notify_change()
    
    # Wishlist methods
    def toggle_wishlist(self, item: Pet | Service):
        """Add or remove item from wishlist"""
        existing = next((i for i in self.wishlist if i.id == item.id), None)
        if existing:
            self.wishlist.remove(existing)
        else:
            self.wishlist.append(item)
        self.notify_change()
    
    def is_in_wishlist(self, item_id: str) -> bool:
        """Check if item is in wishlist"""
        return any(i.id == item_id for i in self.wishlist)
    
    # Cart methods
    def add_to_cart(self, product: Product):
        """Add product to cart"""
        existing = next((item for item in self.cart if item.id == product.id), None)
        if existing:
            existing.quantity += 1
        else:
            self.cart.append(CartItem(
                id=product.id,
                name=product.name,
                price=product.price,
                image=product.image,
                quantity=1
            ))
        self.notify_change()
    
    def remove_from_cart(self, product_id: str):
        """Remove product from cart"""
        self.cart = [item for item in self.cart if item.id != product_id]
        self.notify_change()
    
    def update_cart_quantity(self, product_id: str, new_quantity: int):
        """Update cart item quantity"""
        if new_quantity <= 0:
            self.remove_from_cart(product_id)
        else:
            for item in self.cart:
                if item.id == product_id:
                    item.quantity = new_quantity
                    break
        self.notify_change()
    
    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.clear()
        self.notify_change()
    
    # Booking methods
    def add_booking(self, booking: Booking):
        """Add a new booking"""
        self.bookings.append(booking)
        self.notify_change()
    
    def is_slot_booked(self, service_id: str, date: str, time_slot: str) -> bool:
        """Check if a time slot is already booked"""
        return any(
            b.service_id == service_id and b.date == date and b.time_slot == time_slot
            for b in self.bookings
        )
    
    def get_user_bookings(self) -> List[Booking]:
        """Get bookings for the current user"""
        if not self.current_user:
            return []
        return [b for b in self.bookings if hasattr(b, 'user_id') and b.user_id == self.current_user.id]
    
    def cancel_booking(self, booking_id: str):
        """Cancel a booking"""
        for booking in self.bookings:
            if booking.id == booking_id:
                booking.status = "cancelled"
                break
        self.notify_change()
    
    # Auth methods
    def signup(self, email: str, password: str) -> bool:
        """Sign up a new user"""
        # Load existing users
        users_data = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
        
        # Check if user exists
        if any(u['email'] == email for u in users_data):
            self.add_toast('An account with this email already exists.', 'error')
            return False
        
        # Create new user
        new_user = User(
            id=str(int(datetime.now().timestamp())),
            email=email,
            username=email.split('@')[0],
            profile_picture='assets/default_profile.png',
            password=password
        )
        
        self.current_user = new_user
        self._save_users()
        self.is_auth_modal_open = False
        self.is_profile_modal_open = True
        self.notify_change()
        return True
    
    def login(self, email: str, password: str) -> bool:
        """Log in an existing user"""
        users_data = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
        
        user_data = next((u for u in users_data if u['email'] == email and u['password'] == password), None)
        
        if user_data:
            self.current_user = User(**{k: v for k, v in user_data.items() if k != 'is_current'})
            self._save_users()
            self.is_auth_modal_open = False
            self.add_toast(f'Welcome back, {self.current_user.username}!', 'success')
            self.notify_change()
            return True
        else:
            self.add_toast('Invalid email or password.', 'error')
            return False
    
    def social_login(self, provider: str):
        """Simulate social login"""
        import random
        
        mock_data = {
            'google': {
                'email': f'jane.doe.{random.randint(1, 10000)}@google.com',
                'username': 'Jane Doe',
                'profile_picture': 'assets/default_profile.png'
            },
            'facebook': {
                'email': f'john.smith.{random.randint(1, 10000)}@facebook.com',
                'username': 'John Smith',
                'profile_picture': 'assets/default_profile.png'
            }
        }
        
        data = mock_data.get(provider, mock_data['google'])
        
        # Check if user exists
        users_data = []
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
        
        user_data = next((u for u in users_data if f'@{provider}.com' in u['email']), None)
        
        if user_data:
            self.current_user = User(**{k: v for k, v in user_data.items() if k != 'is_current'})
            self.add_toast(f'Welcome back, {self.current_user.username}!', 'success')
        else:
            self.current_user = User(
                id=str(int(datetime.now().timestamp())),
                email=data['email'],
                username=data['username'],
                profile_picture=data['profile_picture'],
                password=''
            )
            self.is_profile_modal_open = True
            self.add_toast('Account created successfully! Please review your profile.', 'success')
        
        self._save_users()
        self.is_auth_modal_open = False
        self.notify_change()
    
    def logout(self):
        """Log out current user"""
        self.current_user = None
        # Update users file
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users_data = json.load(f)
            for user in users_data:
                user['is_current'] = False
            with open(self.users_file, 'w') as f:
                json.dump(users_data, f, indent=2)
        self.add_toast('You have been signed out.', 'info')
        self.notify_change()
    
    def update_user_profile(self, user_id: str, username: str = None, profile_picture: str = None):
        """Update user profile"""
        if self.current_user and self.current_user.id == user_id:
            if username:
                self.current_user.username = username
            if profile_picture:
                self.current_user.profile_picture = profile_picture
            
            self._save_users()
            self.add_toast('Profile updated successfully!', 'success')
            self.notify_change()

# Global app state instance
app_state = AppState()
