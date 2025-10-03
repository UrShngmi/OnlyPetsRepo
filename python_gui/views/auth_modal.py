"""
Authentication modal for login and signup
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *

class AuthModal(ctk.CTkToplevel):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.mode = "login"  # "login" or "signup"
        
        # Configure modal
        self.title("Sign In / Sign Up")
        self.geometry("500x650")
        self.resizable(False, False)
        
        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (650 // 2)
        self.geometry(f"500x650+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self.configure(fg_color=BG_SECONDARY)
        
        self._create_widgets()
        
        # Bind escape to close
        self.bind("<Escape>", lambda e: self._close())
    
    def _create_widgets(self):
        """Create modal widgets"""
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Tab buttons
        tab_frame = ctk.CTkFrame(container, fg_color="transparent", height=50)
        tab_frame.pack(fill="x", pady=(0, 20))
        tab_frame.pack_propagate(False)
        
        self.login_tab = ctk.CTkButton(
            tab_frame,
            text="Login",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="transparent",
            text_color=YELLOW_PRIMARY,
            hover=False,
            corner_radius=0,
            command=lambda: self._switch_mode("login")
        )
        self.login_tab.pack(side="left", fill="both", expand=True)
        
        self.signup_tab = ctk.CTkButton(
            tab_frame,
            text="Sign Up",
            font=ctk.CTkFont(size=18),
            fg_color="transparent",
            text_color=TEXT_GRAY_400,
            hover=False,
            corner_radius=0,
            command=lambda: self._switch_mode("signup")
        )
        self.signup_tab.pack(side="left", fill="both", expand=True)
        
        # Tab indicator
        self.tab_indicator = ctk.CTkFrame(tab_frame, fg_color=YELLOW_PRIMARY, height=2)
        self.tab_indicator.place(relx=0, rely=1, relwidth=0.5)
        
        # Social login buttons
        google_btn = ctk.CTkButton(
            container,
            text="🌐 Sign in with Google",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=TEXT_WHITE,
            hover_color="#e5e5e5",
            text_color="black",
            height=45,
            corner_radius=8,
            command=lambda: self._social_login("google")
        )
        google_btn.pack(fill="x", pady=(0, 10))
        
        facebook_btn = ctk.CTkButton(
            container,
            text="📘 Continue with Facebook",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1877F2",
            hover_color="#166eab",
            text_color=TEXT_WHITE,
            height=45,
            corner_radius=8,
            command=lambda: self._social_login("facebook")
        )
        facebook_btn.pack(fill="x", pady=(0, 20))
        
        # Divider
        divider_frame = ctk.CTkFrame(container, fg_color="transparent")
        divider_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkFrame(divider_frame, fg_color=BORDER_GRAY, height=1).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(divider_frame, text="OR", text_color=TEXT_GRAY_500, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        ctk.CTkFrame(divider_frame, fg_color=BORDER_GRAY, height=1).pack(side="left", fill="x", expand=True)
        
        # Form container
        self.form_container = ctk.CTkFrame(container, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True)
        
        self._create_login_form()
    
    def _switch_mode(self, mode):
        """Switch between login and signup"""
        self.mode = mode
        
        if mode == "login":
            self.login_tab.configure(text_color=YELLOW_PRIMARY, font=ctk.CTkFont(size=18, weight="bold"))
            self.signup_tab.configure(text_color=TEXT_GRAY_400, font=ctk.CTkFont(size=18))
            self.tab_indicator.place(relx=0, rely=1, relwidth=0.5)
        else:
            self.login_tab.configure(text_color=TEXT_GRAY_400, font=ctk.CTkFont(size=18))
            self.signup_tab.configure(text_color=YELLOW_PRIMARY, font=ctk.CTkFont(size=18, weight="bold"))
            self.tab_indicator.place(relx=0.5, rely=1, relwidth=0.5)
        
        # Clear and recreate form
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        if mode == "login":
            self._create_login_form()
        else:
            self._create_signup_form()
    
    def _create_login_form(self):
        """Create login form"""
        self.email_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Email",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        self.password_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Password",
            show="*",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.password_entry.pack(fill="x", pady=(0, 25))
        
        login_btn = ctk.CTkButton(
            self.form_container,
            text="Login",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            corner_radius=8,
            command=self._handle_login
        )
        login_btn.pack(fill="x")
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
    
    def _create_signup_form(self):
        """Create signup form"""
        self.fullname_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Full Name",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.fullname_entry.pack(fill="x", pady=(0, 15))
        
        self.email_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Email",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        self.password_entry = ctk.CTkEntry(
            self.form_container,
            placeholder_text="Password",
            show="*",
            font=ctk.CTkFont(size=14),
            fg_color=BG_PRIMARY,
            border_color=BORDER_GRAY,
            height=45
        )
        self.password_entry.pack(fill="x", pady=(0, 25))
        
        signup_btn = ctk.CTkButton(
            self.form_container,
            text="Create Account",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=YELLOW_PRIMARY,
            hover_color=YELLOW_HOVER,
            text_color="black",
            height=45,
            corner_radius=8,
            command=self._handle_signup
        )
        signup_btn.pack(fill="x")
        
        # Bind Enter key
        self.password_entry.bind("<Return>", lambda e: self._handle_signup())
    
    def _handle_login(self):
        """Handle login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate email format
        if not email:
            app_state.add_toast("Please enter your email address.", "error")
            return
        
        if "@" not in email or "." not in email.split("@")[-1]:
            app_state.add_toast("Please enter a valid email address.", "error")
            return
        
        # Validate password
        if not password:
            app_state.add_toast("Please enter your password.", "error")
            return
        
        if len(password) < 6:
            app_state.add_toast("Password must be at least 6 characters long.", "error")
            return
        
        success = app_state.login(email, password)
        if success:
            self._close()
    
    def _handle_signup(self):
        """Handle signup"""
        fullname = self.fullname_entry.get().strip() if hasattr(self, 'fullname_entry') else ""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        # Validate full name
        if fullname and len(fullname) < 2:
            app_state.add_toast("Please enter a valid full name (at least 2 characters).", "error")
            return
        
        # Validate email format
        if not email:
            app_state.add_toast("Please enter your email address.", "error")
            return
        
        if "@" not in email or "." not in email.split("@")[-1]:
            app_state.add_toast("Please enter a valid email address.", "error")
            return
        
        # Validate password strength
        if not password:
            app_state.add_toast("Please enter a password.", "error")
            return
        
        if len(password) < 8:
            app_state.add_toast("Password must be at least 8 characters long.", "error")
            return
        
        if not any(c.isupper() for c in password):
            app_state.add_toast("Password must contain at least one uppercase letter.", "error")
            return
        
        if not any(c.islower() for c in password):
            app_state.add_toast("Password must contain at least one lowercase letter.", "error")
            return
        
        if not any(c.isdigit() for c in password):
            app_state.add_toast("Password must contain at least one number.", "error")
            return
        
        success = app_state.signup(email, password)
        if success:
            self._close()
    
    def _social_login(self, provider):
        """Handle social login"""
        app_state.social_login(provider)
        self._close()
    
    def _close(self):
        """Close modal"""
        app_state.is_auth_modal_open = False
        app_state.notify_change()
        self.destroy()
