"""
Service card component
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from models.types import Service
from utils.colors import *

class ServiceCard(ctk.CTkFrame):
    def __init__(self, parent, service: Service, app):
        super().__init__(
            parent,
            fg_color=BG_SECONDARY,
            corner_radius=20,
            cursor="hand2"
        )
        self.service = service
        self.app = app
        self.is_expanded = False
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create card widgets"""
        # Background image layer
        self.bg_frame = ctk.CTkFrame(
            self,
            fg_color=BG_DARK,
            corner_radius=0,
            height=450
        )
        self.bg_frame.pack(fill="both", expand=True)
        self.bg_frame.pack_propagate(False)
        
        # Try to load background image
        self._load_background()
        
        # Overlay
        overlay = ctk.CTkFrame(
            self.bg_frame,
            fg_color="#0a0a0a",  # Dark overlay effect
            corner_radius=0
        )
        overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Content on top
        content_frame = ctk.CTkFrame(overlay, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Service name
        name_label = ctk.CTkLabel(
            content_frame,
            text=self.service.name,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w",
            wraplength=280
        )
        name_label.pack(fill="x", pady=(0, 12))
        
        # Duration
        duration_text = f"{self.service.duration // 60} hours" if self.service.duration > 60 else f"{self.service.duration} minutes"
        duration_label = ctk.CTkLabel(
            content_frame,
            text=duration_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=YELLOW_PRIMARY,
            anchor="w"
        )
        duration_label.pack(fill="x", pady=(0, 8))
        
        # Description
        desc_label = ctk.CTkLabel(
            content_frame,
            text=self.service.description,
            font=ctk.CTkFont(size=15),
            text_color=TEXT_GRAY_300,
            anchor="w",
            wraplength=280
        )
        desc_label.pack(fill="x", pady=(0, 15))
        
        # Activities (show all)
        activities_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        activities_frame.pack(fill="x", pady=(0, 15))
        
        # Show all activities
        for activity in self.service.activities:
            activity_row = ctk.CTkFrame(activities_frame, fg_color="transparent")
            activity_row.pack(fill="x", pady=3)
            
            check_icon = ctk.CTkLabel(
                activity_row,
                text="✓",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=YELLOW_PRIMARY,
                width=25
            )
            check_icon.pack(side="left")
            
            activity_label = ctk.CTkLabel(
                activity_row,
                text=activity,
                font=ctk.CTkFont(size=13),
                text_color=TEXT_GRAY_300,
                anchor="w"
            )
            activity_label.pack(side="left", fill="x")
        
        # Spacer (smaller to ensure button visibility)
        spacer = ctk.CTkFrame(content_frame, fg_color="transparent", height=20)
        spacer.pack(fill="x")
        
        # Bottom row: Price and Book button
        bottom_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        bottom_frame.pack(fill="x", pady=(10, 0))
        
        # Price
        price_label = ctk.CTkLabel(
            bottom_frame,
            text=f"₱{self.service.price:.2f}",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=YELLOW_PRIMARY
        )
        price_label.pack(side="left")
        
        # Book button
        book_btn = ctk.CTkButton(
            bottom_frame,
            text="BOOK NOW",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            width=140,
            corner_radius=10,
            command=self._book
        )
        book_btn.pack(side="right")
    
    def _load_background(self):
        """Load background image"""
        if os.path.exists(self.service.image_url):
            try:
                img = Image.open(self.service.image_url)
                img = img.resize((350, 400), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                bg_label = ctk.CTkLabel(self.bg_frame, image=photo, text="")
                bg_label.image = photo
                bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)
            except:
                pass
    
    def _book(self):
        """Navigate to booking page"""
        self.app.navigate_to("booking", booking_type="service", booking_id=self.service.id)
