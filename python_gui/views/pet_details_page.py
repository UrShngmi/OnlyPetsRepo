"""
Pet details page with image carousel and adoption button
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from utils.colors import *

class PetDetailsPage(ctk.CTkFrame):
    def __init__(self, parent, app, pet_id):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        print(f"PetDetailsPage: Looking for pet with ID: {pet_id}")  # Debug
        self.pet = next((p for p in app_state.pets if p.id == pet_id), None)
        self.active_image_index = 0
        
        if not self.pet:
            print(f"PetDetailsPage: Pet not found with ID: {pet_id}")  # Debug
            print(f"Available pets: {[p.id for p in app_state.pets]}")  # Debug
            # Pet not found, go back to adoption
            self.app.navigate_to("adoption")
            return
        
        print(f"PetDetailsPage: Found pet: {self.pet.name}")  # Debug
        self._create_widgets()
    
    def _create_widgets(self):
        """Create pet details widgets"""
        # Container with dark background
        container = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=20)
        container.pack(fill="both", expand=True)
        
        # Title section
        title_label = ctk.CTkLabel(
            container,
            text=f"ABOUT {self.pet.name.upper()}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=TEXT_GRAY_300,
            anchor="w"
        )
        title_label.pack(fill="x", padx=50, pady=(40, 40))
        
        # Main content grid
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=50, pady=(0, 40))
        
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left: Image carousel
        image_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        image_container.grid(row=0, column=0, sticky="nsew", padx=(0, 30))
        
        self.image_display = ctk.CTkFrame(
            image_container,
            fg_color=BG_SECONDARY,
            corner_radius=20,
            width=400,
            height=400
        )
        self.image_display.pack(pady=20)
        self.image_display.pack_propagate(False)
        
        self._display_image()
        
        # Image navigation dots
        dots_frame = ctk.CTkFrame(image_container, fg_color="transparent")
        dots_frame.pack(pady=10)
        
        self.dot_buttons = []
        for i in range(len(self.pet.image_urls)):
            dot = ctk.CTkButton(
                dots_frame,
                text="●",
                font=ctk.CTkFont(size=16),
                fg_color="transparent",
                hover_color=BG_DARK,
                text_color=YELLOW_PRIMARY if i == 0 else TEXT_GRAY_500,
                width=30,
                height=20,
                command=lambda idx=i: self._change_image(idx)
            )
            dot.pack(side="left", padx=3)
            self.dot_buttons.append(dot)
        
        # Right: Pet information
        info_container = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_container.grid(row=0, column=1, sticky="nsew")
        
        # Pet name (large)
        name_label = ctk.CTkLabel(
            info_container,
            text=self.pet.name.upper(),
            font=ctk.CTkFont(size=56, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # Breed
        breed_label = ctk.CTkLabel(
            info_container,
            text=self.pet.breed,
            font=ctk.CTkFont(size=22),
            text_color=TEXT_GRAY_400,
            anchor="w"
        )
        breed_label.pack(fill="x", pady=(5, 0))
        
        # Age
        age_label = ctk.CTkLabel(
            info_container,
            text=f"{self.pet.age} year{'s' if self.pet.age > 1 else ''} old",
            font=ctk.CTkFont(size=18),
            text_color=YELLOW_PRIMARY,
            anchor="w"
        )
        age_label.pack(fill="x", pady=(10, 20))
        
        # Description
        desc_label = ctk.CTkLabel(
            info_container,
            text=self.pet.description,
            font=ctk.CTkFont(size=15),
            text_color=TEXT_GRAY_300,
            anchor="w",
            justify="left",
            wraplength=450
        )
        desc_label.pack(fill="x", pady=(0, 20))
        
        # Quick facts
        facts_frame = ctk.CTkFrame(info_container, fg_color="transparent")
        facts_frame.pack(fill="x", pady=(0, 30))
        
        for fact in self.pet.quick_facts:
            fact_row = ctk.CTkFrame(facts_frame, fg_color="transparent")
            fact_row.pack(fill="x", pady=3)
            
            check_icon = ctk.CTkLabel(
                fact_row,
                text="✓",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=YELLOW_PRIMARY,
                width=30
            )
            check_icon.pack(side="left")
            
            fact_label = ctk.CTkLabel(
                fact_row,
                text=fact,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_GRAY_400,
                anchor="w"
            )
            fact_label.pack(side="left", fill="x", expand=True)
        
        # Spacer
        ctk.CTkFrame(info_container, fg_color="transparent", height=20).pack()
        
        # Adopt button
        adopt_btn = ctk.CTkButton(
            info_container,
            text="ADOPT",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=50,
            width=200,
            corner_radius=10,
            command=self._adopt
        )
        adopt_btn.pack(anchor="w")
    
    def _display_image(self):
        """Display current image"""
        for widget in self.image_display.winfo_children():
            widget.destroy()
        
        image_path = self.pet.image_urls[self.active_image_index]
        
        # Convert relative path to absolute path
        if not os.path.isabs(image_path):
            base_dir = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(base_dir, image_path)
        
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((380, 380), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                image_label = ctk.CTkLabel(self.image_display, image=photo, text="")
                image_label.image = photo
                image_label.pack(expand=True)
                return
            except Exception as e:
                print(f"Error loading image {image_path}: {e}")
        
        self._create_placeholder()
    
    def _create_placeholder(self):
        """Create placeholder image"""
        placeholder = ctk.CTkLabel(
            self.image_display,
            text=f"🐾\n{self.pet.name}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=TEXT_GRAY_500
        )
        placeholder.pack(expand=True)
    
    def _change_image(self, index):
        """Change active image"""
        self.active_image_index = index
        self._display_image()
        
        # Update dots
        for i, dot in enumerate(self.dot_buttons):
            dot.configure(text_color=YELLOW_PRIMARY if i == index else TEXT_GRAY_500)
    
    def _adopt(self):
        """Navigate to adoption booking"""
        self.app.navigate_to("booking", booking_type="pet", booking_id=self.pet.id)
