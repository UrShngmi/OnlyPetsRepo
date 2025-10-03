"""
Wishlist page displaying favorite pets and services
"""
import customtkinter as ctk
from models.app_state import app_state
from models.types import Pet, Service
from utils.colors import *
from views.components.pet_card import PetCard
from views.components.service_card import ServiceCard

class WishlistPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create wishlist page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Your Wishlist",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Your favorite pets and services, all in one place.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        if not app_state.wishlist:
            self._create_empty_wishlist()
        else:
            self._create_wishlist_content()
    
    def _create_empty_wishlist(self):
        """Display empty wishlist message"""
        empty_frame = ctk.CTkFrame(self, fg_color=BG_SECONDARY, corner_radius=20)
        empty_frame.pack(fill="x", pady=50)
        
        ctk.CTkLabel(
            empty_frame,
            text="Your wishlist is empty!",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(pady=(50, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Browse our pets and services to find your new best friend.",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_400
        ).pack(pady=(0, 20))
        
        browse_btn = ctk.CTkButton(
            empty_frame,
            text="Find Pets",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            width=200,
            corner_radius=10,
            command=lambda: self.app.navigate_to("adoption")
        )
        browse_btn.pack(pady=(0, 50))
    
    def _create_wishlist_content(self):
        """Display wishlist items"""
        # Separate pets and services
        pets = [item for item in app_state.wishlist if isinstance(item, Pet)]
        services = [item for item in app_state.wishlist if isinstance(item, Service)]
        
        # Pets section
        if pets:
            pets_title = ctk.CTkLabel(
                self,
                text="Favorite Pets",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color=TEXT_WHITE,
                anchor="w"
            )
            pets_title.pack(fill="x", pady=(0, 20))
            
            pets_grid = ctk.CTkFrame(self, fg_color="transparent")
            pets_grid.pack(fill="x", pady=(0, 60))
            
            for i in range(4):
                pets_grid.grid_columnconfigure(i, weight=1)
            
            for i, pet in enumerate(pets):
                row = i // 4
                col = i % 4
                
                pet_card = PetCard(pets_grid, pet, self.app)
                pet_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        
        # Services section
        if services:
            services_title = ctk.CTkLabel(
                self,
                text="Saved Services",
                font=ctk.CTkFont(size=32, weight="bold"),
                text_color=TEXT_WHITE,
                anchor="w"
            )
            services_title.pack(fill="x", pady=(0, 20))
            
            services_grid = ctk.CTkFrame(self, fg_color="transparent")
            services_grid.pack(fill="x")
            
            for i in range(3):
                services_grid.grid_columnconfigure(i, weight=1)
            
            for i, service in enumerate(services):
                row = i // 3
                col = i % 3
                
                service_card = ServiceCard(services_grid, service, self.app)
                service_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
    
    def refresh(self):
        """Refresh the page"""
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
