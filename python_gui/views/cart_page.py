"""
Shopping cart page
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from utils.colors import *

class CartPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create cart page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Your Cart",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 40))
        
        if not app_state.cart:
            self._create_empty_cart()
        else:
            self._create_cart_content()
    
    def _create_empty_cart(self):
        """Display empty cart message"""
        empty_frame = ctk.CTkFrame(self, fg_color=BG_SECONDARY, corner_radius=20)
        empty_frame.pack(fill="x", pady=50)
        
        ctk.CTkLabel(
            empty_frame,
            text="Your Cart is Empty",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(pady=(50, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Looks like you haven't added anything to your cart yet.",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_400
        ).pack(pady=(0, 20))
        
        browse_btn = ctk.CTkButton(
            empty_frame,
            text="Browse Products",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            width=200,
            corner_radius=10,
            command=lambda: self.app.navigate_to("products")
        )
        browse_btn.pack(pady=(0, 50))
    
    def _create_cart_content(self):
        """Display cart items and summary"""
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        content_frame.grid_columnconfigure(0, weight=2)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Left: Cart items
        items_frame = ctk.CTkFrame(content_frame, fg_color=BG_DARK, corner_radius=20)
        items_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        
        items_header = ctk.CTkLabel(
            items_frame,
            text="Cart Items",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        items_header.pack(fill="x", padx=30, pady=(30, 20))
        
        # Scrollable items
        items_scroll = ctk.CTkScrollableFrame(
            items_frame,
            fg_color="transparent",
            scrollbar_button_color=BORDER_GRAY
        )
        items_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        for item in app_state.cart:
            self._create_cart_item(items_scroll, item)
        
        # Right: Order summary
        summary_frame = ctk.CTkFrame(content_frame, fg_color=BG_DARK, corner_radius=20)
        summary_frame.grid(row=0, column=1, sticky="nsew")
        
        summary_title = ctk.CTkLabel(
            summary_frame,
            text="Order Summary",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_WHITE
        )
        summary_title.pack(pady=(30, 20), padx=30)
        
        # Calculate totals
        subtotal = sum(item.price * item.quantity for item in app_state.cart)
        taxes = subtotal * 0.1
        total = subtotal + taxes
        
        # Subtotal
        subtotal_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        subtotal_row.pack(fill="x", padx=30, pady=5)
        
        ctk.CTkLabel(
            subtotal_row,
            text="Subtotal",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300
        ).pack(side="left")
        
        ctk.CTkLabel(
            subtotal_row,
            text=f"₱{subtotal:.2f}",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300
        ).pack(side="right")
        
        # Taxes
        taxes_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        taxes_row.pack(fill="x", padx=30, pady=5)
        
        ctk.CTkLabel(
            taxes_row,
            text="Taxes (10%)",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300
        ).pack(side="left")
        
        ctk.CTkLabel(
            taxes_row,
            text=f"₱{taxes:.2f}",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300
        ).pack(side="right")
        
        # Divider
        ctk.CTkFrame(summary_frame, fg_color=BORDER_GRAY, height=1).pack(fill="x", padx=30, pady=20)
        
        # Total
        total_row = ctk.CTkFrame(summary_frame, fg_color="transparent")
        total_row.pack(fill="x", padx=30, pady=5)
        
        ctk.CTkLabel(
            total_row,
            text="Total",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(side="left")
        
        ctk.CTkLabel(
            total_row,
            text=f"₱{total:.2f}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_WHITE
        ).pack(side="right")
        
        # Checkout button
        checkout_btn = ctk.CTkButton(
            summary_frame,
            text="Proceed to Checkout",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=50,
            corner_radius=10,
            command=self._checkout
        )
        checkout_btn.pack(fill="x", padx=30, pady=(20, 30))
    
    def _create_cart_item(self, parent, item):
        """Create a cart item row"""
        item_frame = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=15)
        item_frame.pack(fill="x", pady=8)
        
        content = ctk.CTkFrame(item_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Image (small)
        image_frame = ctk.CTkFrame(content, fg_color=BG_DARK, width=80, height=80, corner_radius=8)
        image_frame.pack(side="left", padx=(0, 15))
        image_frame.pack_propagate(False)
        
        if os.path.exists(item.image):
            try:
                img = Image.open(item.image)
                img = img.resize((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                img_label = ctk.CTkLabel(image_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(expand=True)
            except:
                ctk.CTkLabel(image_frame, text="🛍️", font=ctk.CTkFont(size=24)).pack(expand=True)
        else:
            ctk.CTkLabel(image_frame, text="🛍️", font=ctk.CTkFont(size=24)).pack(expand=True)
        
        # Info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=item.name,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        ).pack(fill="x")
        
        ctk.CTkLabel(
            info_frame,
            text=f"₱{item.price:.2f}",
            font=ctk.CTkFont(size=14),
            text_color=YELLOW_PRIMARY,
            anchor="w"
        ).pack(fill="x", pady=(5, 0))
        
        # Quantity controls
        qty_frame = ctk.CTkFrame(content, fg_color="transparent")
        qty_frame.pack(side="left", padx=15)
        
        ctk.CTkButton(
            qty_frame,
            text="-",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=BORDER_GRAY,
            hover_color=HOVER_GRAY,
            width=35,
            height=35,
            command=lambda: self._update_quantity(item.id, item.quantity - 1)
        ).pack(side="left", padx=3)
        
        ctk.CTkLabel(
            qty_frame,
            text=str(item.quantity),
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_WHITE,
            width=35
        ).pack(side="left", padx=3)
        
        ctk.CTkButton(
            qty_frame,
            text="+",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=BORDER_GRAY,
            hover_color=HOVER_GRAY,
            width=35,
            height=35,
            command=lambda: self._update_quantity(item.id, item.quantity + 1)
        ).pack(side="left", padx=3)
        
        # Total price
        total_price = item.price * item.quantity
        ctk.CTkLabel(
            content,
            text=f"₱{total_price:.2f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_WHITE,
            width=100
        ).pack(side="left", padx=15)
        
        # Remove button
        ctk.CTkButton(
            content,
            text="×",
            font=ctk.CTkFont(size=24, weight="bold"),
            fg_color="transparent",
            hover_color=RED_ERROR,
            text_color=TEXT_GRAY_400,
            width=35,
            height=35,
            command=lambda: self._remove_item(item.id)
        ).pack(side="left")
    
    def _update_quantity(self, product_id, new_quantity):
        """Update item quantity"""
        app_state.update_cart_quantity(product_id, new_quantity)
        self._refresh()
    
    def _remove_item(self, product_id):
        """Remove item from cart"""
        app_state.remove_from_cart(product_id)
        self._refresh()
    
    def _checkout(self):
        """Handle checkout"""
        app_state.add_toast("Checkout successful! Thank you for your order. (Simulated)", "success")
        app_state.clear_cart()
        self._refresh()
    
    def _refresh(self):
        """Refresh the page"""
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
