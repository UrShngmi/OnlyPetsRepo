"""
Contact page with form
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *

class ContactPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create contact page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Get In Touch",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="We'd love to hear from you!",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        # Content container
        content_frame = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=20)
        content_frame.pack(fill="both", expand=True)
        
        # Grid layout
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left: Contact form
        form_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        form_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        
        form_title = ctk.CTkLabel(
            form_frame,
            text="Send us a Message",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        form_title.pack(fill="x", pady=(0, 25))
        
        # Name field
        self.name_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Your Name",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        # Email field
        self.email_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Your Email",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        # Message field
        self.message_text = ctk.CTkTextbox(
            form_frame,
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=150
        )
        self.message_text.pack(fill="x", pady=(0, 20))
        self.message_text.insert("1.0", "Your Message")
        self.message_text.bind("<FocusIn>", self._clear_placeholder)
        
        # Submit button
        submit_btn = ctk.CTkButton(
            form_frame,
            text="Send Message",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=50,
            corner_radius=10,
            command=self._submit_form
        )
        submit_btn.pack(fill="x")
        
        # Right: Location info
        info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        info_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=40)
        
        info_title = ctk.CTkLabel(
            info_frame,
            text="Our Location",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        info_title.pack(fill="x", pady=(0, 25))
        
        # Map placeholder
        map_frame = ctk.CTkFrame(
            info_frame,
            fg_color=BG_SECONDARY,
            corner_radius=10,
            height=250
        )
        map_frame.pack(fill="x", pady=(0, 25))
        map_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            map_frame,
            text="🗺️\n[Map Placeholder]\n123 Pet Lane, Animal City",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_400,
            justify="center"
        ).pack(expand=True)
        
        # Contact details
        details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        details_frame.pack(fill="x")
        
        details = [
            ("Email:", "contact@onlypets.com"),
            ("Phone:", "(123) 456-7890"),
            ("Hours:", "Mon - Sat, 9am - 6pm")
        ]
        
        for label, value in details:
            detail_row = ctk.CTkFrame(details_frame, fg_color="transparent")
            detail_row.pack(fill="x", pady=8)
            
            ctk.CTkLabel(
                detail_row,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_GRAY_300,
                width=80,
                anchor="w"
            ).pack(side="left")
            
            ctk.CTkLabel(
                detail_row,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_GRAY_300,
                anchor="w"
            ).pack(side="left", fill="x", expand=True)
    
    def _clear_placeholder(self, event):
        """Clear placeholder text on focus"""
        if self.message_text.get("1.0", "end-1c") == "Your Message":
            self.message_text.delete("1.0", "end")
    
    def _submit_form(self):
        """Submit contact form"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        message = self.message_text.get("1.0", "end-1c").strip()
        
        if not name or not email or not message or message == "Your Message":
            app_state.add_toast("Please fill in all fields.", "error")
            return
        
        # Simulate form submission
        app_state.add_toast("Thank you for contacting us! We'll get back to you soon.", "success")
        
        # Clear form
        self.name_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.message_text.delete("1.0", "end")
        self.message_text.insert("1.0", "Your Message")
