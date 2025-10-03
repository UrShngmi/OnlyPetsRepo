"""
Adoption page with search and filters
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *
from views.components.pet_card import PetCard

class AdoptionPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.current_filter = "All"
        self.search_query = ""
        self._create_widgets()
    
    def _create_widgets(self):
        """Create adoption page widgets"""
        # Title section
        title = ctk.CTkLabel(
            self,
            text="MAKE A FRIEND",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Select a pet",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent", width=500)
        search_frame.pack(pady=(0, 30))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search by name, species, or breed...",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45,
            width=500
        )
        self.search_entry.pack(fill="x")
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(pady=(0, 30))
        
        filters = ["All", "Dog", "Cat", "Bird", "Other"]
        self.filter_buttons = {}
        
        for filter_name in filters:
            btn = ctk.CTkButton(
                filter_frame,
                text=filter_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=YELLOW_PRIMARY if filter_name == "All" else BG_SECONDARY,
                hover_color=YELLOW_HOVER if filter_name == "All" else HOVER_GRAY,
                text_color="black" if filter_name == "All" else TEXT_GRAY_300,
                corner_radius=20,
                height=40,
                width=100,
                command=lambda f=filter_name: self._set_filter(f)
            )
            btn.pack(side="left", padx=5)
            self.filter_buttons[filter_name] = btn
        
        # Pets grid
        self.pets_container = ctk.CTkFrame(self, fg_color="transparent")
        self.pets_container.pack(fill="both", expand=True)
        
        self._display_pets()
    
    def _on_search(self, event):
        """Handle search input"""
        self.search_query = self.search_entry.get().lower().strip()
        self._display_pets()
    
    def _set_filter(self, filter_name):
        """Set species filter"""
        self.current_filter = filter_name
        
        # Update button styles
        for fname, btn in self.filter_buttons.items():
            if fname == filter_name:
                btn.configure(
                    fg_color=YELLOW_PRIMARY,
                    hover_color=YELLOW_HOVER,
                    text_color="black"
                )
            else:
                btn.configure(
                    fg_color=BG_SECONDARY,
                    hover_color=HOVER_GRAY,
                    text_color=TEXT_GRAY_300
                )
        
        self._display_pets()
    
    def _display_pets(self):
        """Display filtered pets"""
        # Clear existing pets
        for widget in self.pets_container.winfo_children():
            widget.destroy()
        
        # Filter pets
        filtered_pets = app_state.pets
        
        if self.current_filter != "All":
            filtered_pets = [p for p in filtered_pets if p.species == self.current_filter]
        
        if self.search_query:
            filtered_pets = [
                p for p in filtered_pets
                if self.search_query in p.name.lower() or
                   self.search_query in p.species.lower() or
                   self.search_query in p.breed.lower()
            ]
        
        if not filtered_pets:
            # No results
            no_results = ctk.CTkFrame(
                self.pets_container,
                fg_color=BG_SECONDARY,
                corner_radius=20
            )
            no_results.pack(fill="x", pady=20)
            
            ctk.CTkLabel(
                no_results,
                text="No Pets Found",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=TEXT_WHITE
            ).pack(pady=(40, 10))
            
            ctk.CTkLabel(
                no_results,
                text="Try adjusting your search or filters.",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_GRAY_400
            ).pack(pady=(0, 40))
        else:
            # Display pets in grid
            pets_grid = ctk.CTkFrame(self.pets_container, fg_color="transparent")
            pets_grid.pack(fill="both", expand=True)
            
            cols = 4
            for i in range(cols):
                pets_grid.grid_columnconfigure(i, weight=1)
            
            for i, pet in enumerate(filtered_pets):
                row = i // cols
                col = i % cols
                
                pet_card = PetCard(pets_grid, pet, self.app)
                pet_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
