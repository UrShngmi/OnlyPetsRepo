"""
Home page view
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *
from views.components.pet_card import PetCard

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create home page widgets"""
        # Hero Section
        hero_frame = ctk.CTkFrame(
            self,
            fg_color=BG_DARK,
            corner_radius=20,
            height=500
        )
        hero_frame.pack(fill="x", pady=(0, 80))
        hero_frame.pack_propagate(False)
        
        hero_content = ctk.CTkFrame(hero_frame, fg_color="transparent")
        hero_content.place(relx=0.1, rely=0.5, anchor="w")
        
        hero_title = ctk.CTkLabel(
            hero_content,
            text="Find Your\nForever Friend",
            font=ctk.CTkFont(size=60, weight="bold"),
            text_color=TEXT_WHITE,
            justify="left"
        )
        hero_title.pack(anchor="w", pady=(0, 20))
        
        hero_desc = ctk.CTkLabel(
            hero_content,
            text="At OnlyPets, we connect loving families with pets in need of a home.\nExplore our services and find the perfect companion today.",
            font=ctk.CTkFont(size=18),
            text_color=TEXT_GRAY_300,
            justify="left"
        )
        hero_desc.pack(anchor="w", pady=(0, 30))
        
        # CTA Buttons
        cta_frame = ctk.CTkFrame(hero_content, fg_color="transparent")
        cta_frame.pack(anchor="w")
        
        meet_pets_btn = ctk.CTkButton(
            cta_frame,
            text="Meet The Pets",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            corner_radius=25,
            height=45,
            width=180,
            command=lambda: self.app.navigate_to("adoption")
        )
        meet_pets_btn.pack(side="left", padx=(0, 15))
        
        services_btn = ctk.CTkButton(
            cta_frame,
            text="Our Services",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_GRAY_300,
            border_width=2,
            border_color=BORDER_GRAY_LIGHT,
            corner_radius=25,
            height=45,
            width=180,
            command=lambda: self.app.navigate_to("services")
        )
        services_btn.pack(side="left")
        
        # Why Choose Us Section
        section_title = ctk.CTkLabel(
            self,
            text="Why Choose OnlyPets?",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=TEXT_WHITE
        )
        section_title.pack(pady=(0, 10))
        
        section_desc = ctk.CTkLabel(
            self,
            text="We provide a seamless experience for adoption, top-tier pet services, and a community that cares.",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        section_desc.pack(pady=(0, 40))
        
        # Feature cards
        features_frame = ctk.CTkFrame(self, fg_color="transparent")
        features_frame.pack(fill="x", pady=(0, 80))
        
        features_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        features = [
            ("Find a Friend", "Browse our diverse selection of lovable pets waiting for a forever home."),
            ("Expert Care", "From grooming to health checkups, our professional services ensure your pet is happy and healthy."),
            ("Quality Products", "Shop a curated selection of the best food, toys, and accessories for your companion.")
        ]
        
        for i, (title, desc) in enumerate(features):
            feature_card = ctk.CTkFrame(
                features_frame,
                fg_color=BG_SECONDARY,
                corner_radius=20
            )
            feature_card.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
            
            feature_title = ctk.CTkLabel(
                feature_card,
                text=title,
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=YELLOW_PRIMARY
            )
            feature_title.pack(pady=(30, 15))
            
            feature_desc = ctk.CTkLabel(
                feature_card,
                text=desc,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_GRAY_300,
                wraplength=300
            )
            feature_desc.pack(pady=(0, 30), padx=20)
        
        # Featured Pets Section
        if app_state.pets:
            featured_title = ctk.CTkLabel(
                self,
                text="Featured Pets",
                font=ctk.CTkFont(size=36, weight="bold"),
                text_color=TEXT_WHITE
            )
            featured_title.pack(pady=(0, 40))
            
            pets_grid = ctk.CTkFrame(self, fg_color="transparent")
            pets_grid.pack(fill="x", pady=(0, 80))
            
            for i in range(4):
                pets_grid.grid_columnconfigure(i, weight=1)
            
            # Show first 4 pets
            for i, pet in enumerate(app_state.pets[:4]):
                pet_card = PetCard(pets_grid, pet, self.app)
                pet_card.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
        
        # Testimonials Section
        testimonials_title = ctk.CTkLabel(
            self,
            text="What Our Friends Say",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=TEXT_WHITE
        )
        testimonials_title.pack(pady=(0, 40))
        
        testimonials_frame = ctk.CTkFrame(self, fg_color="transparent")
        testimonials_frame.pack(fill="x")
        
        testimonials_frame.grid_columnconfigure((0, 1), weight=1)
        
        testimonials = [
            ("\"Adopting Buddy from OnlyPets was the best decision we've ever made. The process was so smooth and the staff were incredibly supportive. Our home feels complete now!\"",
             "- The Johnson Family"),
            ("\"I use their grooming service every month for my poodle, Luna. They do an amazing job every time, and Luna always comes back happy and looking fabulous. Highly recommend!\"",
             "- Sarah L.")
        ]
        
        for i, (quote, author) in enumerate(testimonials):
            testimonial_card = ctk.CTkFrame(
                testimonials_frame,
                fg_color=BG_SECONDARY,
                corner_radius=20
            )
            testimonial_card.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
            
            quote_label = ctk.CTkLabel(
                testimonial_card,
                text=quote,
                font=ctk.CTkFont(size=14, slant="italic"),
                text_color=TEXT_GRAY_300,
                wraplength=450,
                justify="left"
            )
            quote_label.pack(pady=(30, 15), padx=30)
            
            author_label = ctk.CTkLabel(
                testimonial_card,
                text=author,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=YELLOW_PRIMARY
            )
            author_label.pack(pady=(0, 30))
