"""
Products page with product cards
"""
import customtkinter as ctk
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from models.types import Product
from utils.colors import *

class ProductsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.products = [
            Product(id='prod_01', name='Premium Pet Food', price=1500.00, image='assets/products/petfood.png'),
            Product(id='prod_02', name='Nutritious Pet Food', price=1350.00, image='assets/products/petfood.png'),
            Product(id='prod_03', name='Organic Pet Food', price=1800.00, image='assets/products/petfood.png'),
            Product(id='prod_04', name='Gourmet Pet Food', price=2000.00, image='assets/products/petfood.png'),
        ]
        self._create_widgets()
    
    def _create_widgets(self):
        """Create products page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Pet Products",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="Everything your furry friend needs",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        # Products grid
        products_grid = ctk.CTkFrame(self, fg_color="transparent")
        products_grid.pack(fill="both", expand=True)
        
        for i in range(4):
            products_grid.grid_columnconfigure(i, weight=1)
        
        for i, product in enumerate(self.products):
            col = i % 4
            
            product_card = self._create_product_card(products_grid, product)
            product_card.grid(row=0, column=col, padx=15, pady=15, sticky="nsew")
    
    def _create_product_card(self, parent, product: Product):
        """Create a product card"""
        card = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=20)
        
        # Image
        image_frame = ctk.CTkFrame(card, fg_color=BG_DARK, height=200, corner_radius=0)
        image_frame.pack(fill="x")
        image_frame.pack_propagate(False)
        
        # Convert relative path to absolute path
        image_path = product.image
        if not os.path.isabs(image_path):
            base_dir = os.path.dirname(os.path.dirname(__file__))
            image_path = os.path.join(base_dir, image_path)
        
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((250, 200), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                img_label = ctk.CTkLabel(image_frame, image=photo, text="")
                img_label.image = photo
                img_label.pack(expand=True)
            except Exception as e:
                print(f"Error loading product image {image_path}: {e}")
                self._create_product_placeholder(image_frame, product)
        else:
            print(f"Product image not found: {image_path}")
            self._create_product_placeholder(image_frame, product)
        
        # Content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Product name
        name_label = ctk.CTkLabel(
            content_frame,
            text=product.name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w",
            wraplength=200
        )
        name_label.pack(fill="x")
        
        # Price
        price_label = ctk.CTkLabel(
            content_frame,
            text=f"₱{product.price:.2f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=YELLOW_PRIMARY,
            anchor="w"
        )
        price_label.pack(fill="x", pady=(10, 0))
        
        # Add to cart button
        add_btn = ctk.CTkButton(
            content_frame,
            text="Add to Cart",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=40,
            corner_radius=8,
            command=lambda p=product: self._add_to_cart(p)
        )
        add_btn.pack(fill="x", pady=(15, 0))
        
        return card
    
    def _create_product_placeholder(self, frame, product):
        """Create placeholder for missing product image"""
        placeholder = ctk.CTkLabel(
            frame,
            text=f"🛍️\n{product.name}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_GRAY_500
        )
        placeholder.pack(expand=True)
    
    def _add_to_cart(self, product: Product):
        """Add product to cart"""
        app_state.add_to_cart(product)
        app_state.add_toast(f"{product.name} added to cart!", "success")
