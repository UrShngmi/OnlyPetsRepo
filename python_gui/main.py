import customtkinter as ctk
import tkinter as tk
from tkinter import font as tkfont
import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.app_state import app_state
from utils.colors import *
from views.header import Header
from views.home_page import HomePage
from views.adoption_page import AdoptionPage
from views.pet_details_page import PetDetailsPage
from views.services_page import ServicesPage
from views.products_page import ProductsPage
from views.contact_page import ContactPage
from views.wishlist_page import WishlistPage
from views.cart_page import CartPage
from views.booking_page import BookingPage
from views.manage_bookings_page import ManageBookingsPage
from views.auth_modal import AuthModal
from views.profile_modal import ProfileModal
from views.toast_container import ToastContainer

class OnlyPetsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("OnlyPets - Pet Adoption & Services")
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Set window size to 90% of screen (not full maximized)
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        
        # Center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        # Don't use state('zoomed') - let it be a regular window
        
        # Configure color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Configure main window colors
        self.configure(fg_color=BG_PRIMARY)
        
        # Current page tracking
        self.current_page = None
        self.current_page_name = "home"
        self.current_pet_id = None
        self.current_booking_type = None
        self.current_booking_id = None
        
        # Setup UI
        self._create_widgets()
        
        # Register state change callback
        app_state.on_state_change = self._on_state_change
        
        # Configure window close protocol
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        
        # Show initial page
        self.navigate_to("home")
        
    def _create_widgets(self):
        """Create main UI components"""
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color=BG_PRIMARY)
        self.main_container.pack(fill="both", expand=True)
        
        # Header (sticky at top with backdrop blur effect)
        self.header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=BLACK_OVERLAY,
            corner_radius=0,
            height=80
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Header content container (max width)
        self.header_content = ctk.CTkFrame(
            self.header_frame,
            fg_color="transparent"
        )
        self.header_content.pack(fill="both", padx=50, pady=0)
        
        # Header component
        self.header = Header(self.header_content, self)
        self.header.pack(fill="both", expand=True, pady=15)
        
        # Content area (with max width and centered)
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Scrollable content
        self.content_scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=BORDER_GRAY,
            scrollbar_button_hover_color=BORDER_GRAY_LIGHT
        )
        self.content_scroll.pack(fill="both", expand=True)
        
        # Modal containers (will be shown/hidden)
        self.auth_modal = None
        self.profile_modal = None
        self.toast_container = ToastContainer(self)
    
    def _on_state_change(self):
        """Handle state changes"""
        # Update header
        if hasattr(self, 'header'):
            self.header.update_display()
        
        # Update toast container
        if hasattr(self, 'toast_container'):
            self.toast_container.update_toasts()
        
        # Show/hide auth modal
        if app_state.is_auth_modal_open:
            if not self.auth_modal or not self.auth_modal.winfo_exists():
                self.auth_modal = AuthModal(self, self)
        elif self.auth_modal and self.auth_modal.winfo_exists():
            self.auth_modal.destroy()
            self.auth_modal = None
        
        # Show/hide profile modal
        if app_state.is_profile_modal_open:
            if not self.profile_modal or not self.profile_modal.winfo_exists():
                self.profile_modal = ProfileModal(self, self)
        elif self.profile_modal and self.profile_modal.winfo_exists():
            self.profile_modal.destroy()
            self.profile_modal = None
        
        # Refresh current page if needed
        if self.current_page and hasattr(self.current_page, 'refresh'):
            self.current_page.refresh()
    
    def navigate_to(self, page_name: str, pet_id: str = None, booking_type: str = None, booking_id: str = None):
        """Navigate to a different page"""
        # Clear current page
        if self.current_page:
            self.current_page.destroy()
        
        # Store navigation params
        self.current_page_name = page_name
        self.current_pet_id = pet_id
        self.current_booking_type = booking_type
        self.current_booking_id = booking_id
        
        # Reset scroll position
        self.content_scroll._parent_canvas.yview_moveto(0)
        
        # Create new page
        if page_name == "home":
            self.current_page = HomePage(self.content_scroll, self)
        elif page_name == "adoption":
            self.current_page = AdoptionPage(self.content_scroll, self)
        elif page_name == "pet_details":
            self.current_page = PetDetailsPage(self.content_scroll, self, pet_id)
        elif page_name == "services":
            self.current_page = ServicesPage(self.content_scroll, self)
        elif page_name == "products":
            self.current_page = ProductsPage(self.content_scroll, self)
        elif page_name == "contact":
            self.current_page = ContactPage(self.content_scroll, self)
        elif page_name == "wishlist":
            self.current_page = WishlistPage(self.content_scroll, self)
        elif page_name == "cart":
            self.current_page = CartPage(self.content_scroll, self)
        elif page_name == "booking":
            self.current_page = BookingPage(self.content_scroll, self, booking_type, booking_id)
        elif page_name == "manage_bookings":
            self.current_page = ManageBookingsPage(self.content_scroll, self)
        
        if self.current_page:
            self.current_page.pack(fill="both", expand=True)
        
        # Update header to reflect active page
        if hasattr(self, 'header'):
            self.header.update_display()
    
    def _on_closing(self):
        """Handle window close event"""
        try:
            # Clean up any resources if needed
            self.quit()  # Stop the mainloop
            self.destroy()  # Destroy the window
        except Exception as e:
            print(f"Error during shutdown: {e}")
            # Force exit if needed
            import sys
            sys.exit(0)

def main():
    """Main entry point"""
    # Check for assets directory
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
        os.makedirs(os.path.join(assets_dir, 'pets'), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, 'services'), exist_ok=True)
        os.makedirs(os.path.join(assets_dir, 'products'), exist_ok=True)
        print("Assets directories created. Please add images to the 'assets' folder.")
    
    app = OnlyPetsApp()
    app.mainloop()

if __name__ == "__main__":
    main()
