"""
Pet card component
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from models.types import Pet
from utils.colors import *

class PetCard(ctk.CTkFrame):
    def __init__(self, parent, pet: Pet, app):
        super().__init__(
            parent,
            fg_color=BG_SECONDARY,
            corner_radius=20,
            cursor="hand2"
        )
        self.pet = pet
        self.app = app
        self.image_label = None
        
        self._create_widgets()
        
        # Bind click to navigate to details
        self.bind("<Button-1>", self._on_click)
        self._bind_click_to_children(self)
    
    def _create_widgets(self):
        """Create card widgets"""
        # Image placeholder
        image_frame = ctk.CTkFrame(
            self,
            fg_color=BG_DARK,
            height=200,
            corner_radius=0
        )
        image_frame.pack(fill="x")
        image_frame.pack_propagate(False)
        
        # Try to load image
        self._load_image(image_frame)
        
        # Content section
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Pet name
        name_label = ctk.CTkLabel(
            content_frame,
            text=self.pet.name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # Breed
        breed_label = ctk.CTkLabel(
            content_frame,
            text=self.pet.breed,
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_400,
            anchor="w"
        )
        breed_label.pack(fill="x", pady=(5, 0))
        
        # Spacer
        spacer = ctk.CTkFrame(content_frame, fg_color="transparent", height=10)
        spacer.pack(fill="x", expand=True)
        
        # View Details button/badge
        details_badge = ctk.CTkLabel(
            content_frame,
            text="View Details",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=YELLOW_PRIMARY,
            fg_color="#3d2f1a",  # Dark yellow background
            corner_radius=15,
            width=100,
            height=30
        )
        details_badge.pack(anchor="w")
        
        # Wishlist button (top right)
        self.wishlist_btn = ctk.CTkButton(
            self,
            text="♥" if app_state.is_in_wishlist(self.pet.id) else "♡",
            font=ctk.CTkFont(size=20),
            fg_color="#1a1a1a",  # semi-transparent effect
            hover_color="#2a2a2a",
            text_color=YELLOW_PRIMARY if app_state.is_in_wishlist(self.pet.id) else TEXT_WHITE,
            width=40,
            height=40,
            corner_radius=20,
            command=self._toggle_wishlist
        )
        self.wishlist_btn.place(relx=0.9, rely=0.05, anchor="center")
    
    def _load_image(self, frame):
        """Load pet image"""
        image_path = self.pet.image_urls[0] if self.pet.image_urls else None
        
        if image_path:
            # Convert relative path to absolute path
            if not os.path.isabs(image_path):
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                image_path = os.path.join(base_dir, image_path)
            
            if os.path.exists(image_path):
                try:
                    img = Image.open(image_path)
                    img = img.resize((300, 200), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    
                    self.image_label = ctk.CTkLabel(
                        frame,
                        image=photo,
                        text=""
                    )
                    self.image_label.image = photo  # Keep reference
                    self.image_label.pack(fill="both", expand=True)
                    return
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
        
        # Fallback to placeholder
        self._create_placeholder(frame)
    
    def _create_placeholder(self, frame):
        """Create placeholder when image not available"""
        placeholder = ctk.CTkLabel(
            frame,
            text=f"🐾\n{self.pet.name}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_GRAY_500
        )
        placeholder.pack(expand=True)
    
    def _bind_click_to_children(self, widget):
        """Recursively bind click event to all child widgets"""
        try:
            for child in widget.winfo_children():
                # Skip the wishlist button
                if child != self.wishlist_btn:
                    child.bind("<Button-1>", self._on_click)
                    self._bind_click_to_children(child)
        except:
            pass  # Some widgets might not support binding
    
    def _toggle_wishlist(self):
        """Toggle wishlist status"""
        app_state.toggle_wishlist(self.pet)
        is_in_wishlist = app_state.is_in_wishlist(self.pet.id)
        self.wishlist_btn.configure(
            text="♥" if is_in_wishlist else "♡",
            text_color=YELLOW_PRIMARY if is_in_wishlist else TEXT_WHITE
        )
        message = f"{self.pet.name} {'added to' if is_in_wishlist else 'removed from'} wishlist!"
        app_state.add_toast(message, 'success')
    
    def _on_click(self, event):
        """Handle card click"""
        # Don't navigate if clicking wishlist button
        if hasattr(self, 'wishlist_btn') and event.widget == self.wishlist_btn:
            return
        
        self.app.navigate_to("pet_details", pet_id=self.pet.id)
