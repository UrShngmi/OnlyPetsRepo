"""
Header component with navigation and user profile
"""
import customtkinter as ctk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from utils.colors import *

class Header(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.dropdown_open = False
        self.dropdown_menu = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create header widgets"""
        # Logo
        self.logo = ctk.CTkLabel(
            self,
            text="ONLYPETS",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=YELLOW_PRIMARY,
            cursor="hand2"
        )
        self.logo.pack(side="left", padx=10)
        self.logo.bind("<Button-1>", lambda e: self.app.navigate_to("home"))
        
        # Navigation links (center)
        self.nav_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.nav_frame.pack(side="left", expand=True)
        
        nav_items = [
            ("Home", "home"),
            ("Adoption", "adoption"),
            ("Services", "services"),
            ("Products", "products"),
            ("Contact", "contact")
        ]
        
        self.nav_buttons = {}
        for text, page in nav_items:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=text,
                fg_color="transparent",
                hover_color=HOVER_GRAY,
                text_color=TEXT_GRAY_300,
                font=ctk.CTkFont(size=14, weight="normal"),
                width=80,
                height=35,
                corner_radius=8,
                command=lambda p=page: self._nav_click(p)
            )
            btn.pack(side="left", padx=5)
            self.nav_buttons[page] = btn
        
        # Right side: Wishlist, Cart, Auth/Profile
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.pack(side="right", padx=10)
        
        # Wishlist button
        self.wishlist_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.wishlist_frame.pack(side="left", padx=10)
        
        self.wishlist_btn = ctk.CTkButton(
            self.wishlist_frame,
            text="♥",
            font=ctk.CTkFont(size=20),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_GRAY_300,
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: self.app.navigate_to("wishlist")
        )
        self.wishlist_btn.pack(side="left")
        
        self.wishlist_badge = None
        
        # Cart button
        self.cart_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.cart_frame.pack(side="left", padx=10)
        
        self.cart_btn = ctk.CTkButton(
            self.cart_frame,
            text="🛒",
            font=ctk.CTkFont(size=18),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_GRAY_300,
            width=40,
            height=40,
            corner_radius=8,
            command=lambda: self.app.navigate_to("cart")
        )
        self.cart_btn.pack(side="left")
        
        self.cart_badge = None
        
        # Auth/Profile section
        self.auth_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.auth_frame.pack(side="left", padx=10)
        
        self.auth_button = None
        self.profile_button = None
        
        self.update_display()
    
    def _nav_click(self, page):
        """Handle navigation click"""
        self.app.navigate_to(page)
    
    def update_display(self):
        """Update header display based on state"""
        # Update navigation button states
        for page, btn in self.nav_buttons.items():
            if page == self.app.current_page_name:
                btn.configure(
                    fg_color=YELLOW_PRIMARY,
                    text_color="black",
                    font=ctk.CTkFont(size=14, weight="bold")
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=TEXT_GRAY_300,
                    font=ctk.CTkFont(size=14, weight="normal")
                )
        
        # Update wishlist badge
        wishlist_count = len(app_state.wishlist)
        if self.wishlist_badge:
            self.wishlist_badge.destroy()
            self.wishlist_badge = None
        
        if wishlist_count > 0:
            self.wishlist_badge = ctk.CTkLabel(
                self.wishlist_frame,
                text=str(wishlist_count),
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                text_color="black",
                width=20,
                height=20,
                corner_radius=10
            )
            self.wishlist_badge.place(relx=0.7, rely=0.2, anchor="center")
        
        # Update cart badge
        cart_count = sum(item.quantity for item in app_state.cart)
        if self.cart_badge:
            self.cart_badge.destroy()
            self.cart_badge = None
        
        if cart_count > 0:
            self.cart_badge = ctk.CTkLabel(
                self.cart_frame,
                text=str(cart_count),
                font=ctk.CTkFont(size=10, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                text_color="black",
                width=20,
                height=20,
                corner_radius=10
            )
            self.cart_badge.place(relx=0.7, rely=0.2, anchor="center")
        
        # Update auth/profile section
        if self.auth_button:
            self.auth_button.destroy()
            self.auth_button = None
        if self.profile_button:
            self.profile_button.destroy()
            self.profile_button = None
        
        if app_state.current_user:
            # Show profile button with dropdown
            self.profile_button = ctk.CTkButton(
                self.auth_frame,
                text=f"👤 {app_state.current_user.username}",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                hover_color=HOVER_GRAY,
                text_color=TEXT_WHITE,
                border_width=2,
                border_color=YELLOW_PRIMARY,
                corner_radius=20,
                height=35,
                command=self._toggle_dropdown
            )
            self.profile_button.pack()
        else:
            # Show sign in/sign up button
            self.auth_button = ctk.CTkButton(
                self.auth_frame,
                text="Sign In / Sign Up",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent",
                hover_color=YELLOW_PRIMARY,
                text_color=YELLOW_PRIMARY,
                border_width=2,
                border_color=YELLOW_PRIMARY,
                corner_radius=20,
                height=35,
                command=self._open_auth_modal
            )
            self.auth_button.pack()
    
    def _open_auth_modal(self):
        """Open authentication modal"""
        app_state.is_auth_modal_open = True
        app_state.notify_change()
    
    def _toggle_dropdown(self):
        """Toggle profile dropdown menu"""
        if self.dropdown_open:
            self._close_dropdown()
        else:
            self._open_dropdown()
    
    def _open_dropdown(self):
        """Open dropdown menu"""
        if self.dropdown_menu:
            self.dropdown_menu.destroy()
        
        # Get position relative to window
        x = self.profile_button.winfo_rootx() - self.winfo_rootx()
        y = self.profile_button.winfo_rooty() - self.winfo_rooty() + self.profile_button.winfo_height() + 5
        
        # Create dropdown
        self.dropdown_menu = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=BG_SECONDARY,
            corner_radius=8,
            border_width=1,
            border_color=BORDER_GRAY
        )
        
        # Manage Bookings button
        manage_bookings_btn = ctk.CTkButton(
            self.dropdown_menu,
            text="📅 Manage Bookings",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_GRAY_300,
            anchor="w",
            command=self._manage_bookings
        )
        manage_bookings_btn.pack(fill="x", padx=10, pady=(10, 5))
        
        logout_btn = ctk.CTkButton(
            self.dropdown_menu,
            text="🚪 Sign Out",
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_GRAY_300,
            anchor="w",
            command=self._logout
        )
        logout_btn.pack(fill="x", padx=10, pady=(5, 10))
        
        self.dropdown_menu.place(x=x, y=y)
        self.dropdown_open = True
        
        # Bind click outside to close
        self.winfo_toplevel().bind("<Button-1>", self._check_dropdown_click, add="+")
    
    def _check_dropdown_click(self, event):
        """Check if click is outside dropdown"""
        if self.dropdown_menu and self.dropdown_menu.winfo_exists():
            x, y = event.x_root, event.y_root
            dropdown_x = self.dropdown_menu.winfo_rootx()
            dropdown_y = self.dropdown_menu.winfo_rooty()
            dropdown_w = self.dropdown_menu.winfo_width()
            dropdown_h = self.dropdown_menu.winfo_height()
            
            if not (dropdown_x <= x <= dropdown_x + dropdown_w and dropdown_y <= y <= dropdown_y + dropdown_h):
                self._close_dropdown()
    
    def _close_dropdown(self):
        """Close dropdown menu"""
        if self.dropdown_menu:
            self.dropdown_menu.destroy()
            self.dropdown_menu = None
        self.dropdown_open = False
        self.winfo_toplevel().unbind("<Button-1>")
    
    def _manage_bookings(self):
        """Navigate to manage bookings page"""
        self._close_dropdown()
        self.app.navigate_to("manage_bookings")
    
    def _logout(self):
        """Handle logout"""
        self._close_dropdown()
        app_state.logout()
