"""
Profile setup modal
"""
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
from models.app_state import app_state
from utils.colors import *

class ProfileModal(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.selected_image_path = None
        
        # Configure modal
        self.title("Set Up Your Profile")
        self.geometry("450x550")
        self.resizable(False, False)
        
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.winfo_screenheight() // 2) - (550 // 2)
        self.geometry(f"450x550+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=BG_SECONDARY)
        
        self._create_widgets()
        
        # Bind escape to skip
        self.bind("<Escape>", lambda e: self._skip())
    
    def _create_widgets(self):
        """Create modal widgets"""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="Set Up Your Profile",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 10))
        
        subtitle = ctk.CTkLabel(
            container,
            text="Welcome! Personalize your account.",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 30))
        
        # Profile picture
        self.profile_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.profile_frame.pack(pady=(0, 30))
        
        # Load current profile picture
        current_pic = app_state.current_user.profile_picture if app_state.current_user else "assets/default_profile.png"
        
        self.profile_image_label = ctk.CTkLabel(
            self.profile_frame,
            text="👤",
            font=ctk.CTkFont(size=60),
            fg_color=BG_DARK,
            corner_radius=60,
            width=120,
            height=120
        )
        self.profile_image_label.pack()
        
        # Upload button
        upload_btn = ctk.CTkButton(
            self.profile_frame,
            text="📷",
            font=ctk.CTkFont(size=20),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            width=40,
            height=40,
            corner_radius=20,
            command=self._upload_image
        )
        upload_btn.place(relx=0.7, rely=0.7, anchor="center")
        
        # Username entry
        self.username_entry = ctk.CTkEntry(
            container,
            placeholder_text="Enter your display name",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45,
            justify="center"
        )
        self.username_entry.pack(fill="x", pady=(0, 30))
        
        if app_state.current_user:
            self.username_entry.insert(0, app_state.current_user.username)
        
        # Buttons
        buttons_frame = ctk.CTkFrame(container, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        skip_btn = ctk.CTkButton(
            buttons_frame,
            text="Skip for Now",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=BORDER_GRAY,
            hover_color=HOVER_GRAY,
            text_color=TEXT_WHITE,
            height=45,
            corner_radius=8,
            command=self._skip
        )
        skip_btn.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Save Profile",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            corner_radius=8,
            command=self._save
        )
        save_btn.grid(row=0, column=1, padx=(10, 0), sticky="ew")
    
    def _upload_image(self):
        """Upload profile image"""
        file_path = filedialog.askopenfilename(
            title="Select Profile Picture",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        
        if file_path:
            try:
                # Load and display image
                img = Image.open(file_path)
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                self.profile_image_label.configure(image=photo, text="")
                self.profile_image_label.image = photo
                self.selected_image_path = file_path
            except Exception as e:
                app_state.add_toast(f"Error loading image: {e}", "error")
    
    def _save(self):
        """Save profile"""
        if not app_state.current_user:
            self._close()
            return
        
        username = self.username_entry.get().strip()
        if not username:
            app_state.add_toast("Please enter a username.", "error")
            return
        
        # Save to app state
        app_state.update_user_profile(
            app_state.current_user.id,
            username=username,
            profile_picture=self.selected_image_path if self.selected_image_path else app_state.current_user.profile_picture
        )
        
        self._close()
    
    def _skip(self):
        """Skip profile setup"""
        self._close()
    
    def _close(self):
        """Close modal"""
        app_state.is_profile_modal_open = False
        app_state.notify_change()
        self.destroy()
