"""
Services page
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *
from views.components.service_card import ServiceCard

class ServicesPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create services page widgets"""
        
        # Title
        title = ctk.CTkLabel(
            self,
            text="Our Services",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Professional care for your beloved pets",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        # Check if services exist
        if not app_state.services:
            no_services_label = ctk.CTkLabel(
                self,
                text="No services available at the moment.",
                font=ctk.CTkFont(size=18),
                text_color=TEXT_GRAY_400
            )
            no_services_label.pack(pady=50)
            return
        
        # Services grid
        services_grid = ctk.CTkFrame(self, fg_color="transparent")
        services_grid.pack(fill="both", expand=True)
        
        # Configure grid
        for i in range(3):
            services_grid.grid_columnconfigure(i, weight=1)
        
        # Calculate number of rows needed
        num_rows = (len(app_state.services) + 2) // 3
        for i in range(num_rows):
            services_grid.grid_rowconfigure(i, minsize=480)
        
        for i, service in enumerate(app_state.services):
            row = i // 3
            col = i % 3
            
            service_card = ServiceCard(services_grid, service, self.app)
            service_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
