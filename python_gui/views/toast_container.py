"""
Toast notification container
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *

class ToastContainer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent", width=320, height=0)
        self.parent = parent
        self.toasts = {}
        self.is_visible = False
        
        # Start hidden
        self.place_forget()
        
        self.update_toasts()
    
    def update_toasts(self):
        """Update displayed toasts"""
        # Remove toasts that are no longer in state
        toast_ids = [t.id for t in app_state.toasts]
        for toast_id in list(self.toasts.keys()):
            if toast_id not in toast_ids:
                if self.toasts[toast_id].winfo_exists():
                    self.toasts[toast_id].destroy()
                del self.toasts[toast_id]
        
        # Add new toasts
        for toast in app_state.toasts:
            if toast.id not in self.toasts:
                toast_widget = self._create_toast(toast)
                self.toasts[toast.id] = toast_widget
                
                # Auto-remove after 3 seconds
                self.after(3000, lambda tid=toast.id: self._remove_toast(tid))
        
        # Show/hide container based on toast existence
        if self.toasts and not self.is_visible:
            self.place(relx=0.98, rely=0.05, anchor="ne")
            self.lift()  # Bring to front
            self.is_visible = True
        elif not self.toasts and self.is_visible:
            self.place_forget()
            self.is_visible = False
    
    def _create_toast(self, toast):
        """Create a toast widget"""
        # Color based on type
        colors = {
            'success': ("#0d7c4d", "#065f46"),  # Darker green
            'error': ("#b91c1c", "#7f1d1d"),    # Darker red
            'info': ("#2563eb", "#1e3a8a")      # Darker blue
        }
        bg_color, border_color = colors.get(toast.type, colors['info'])
        
        toast_frame = ctk.CTkFrame(
            self,
            fg_color=bg_color,
            border_width=1,
            border_color=border_color,
            corner_radius=6,
            width=350,
            height=50
        )
        toast_frame.pack(pady=5, anchor="e")
        toast_frame.pack_propagate(False)
        
        # Content
        content_frame = ctk.CTkFrame(toast_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=12, pady=8)
        
        message_label = ctk.CTkLabel(
            content_frame,
            text=toast.message,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=TEXT_WHITE,
            wraplength=280,
            justify="left"
        )
        message_label.pack(side="left", fill="both", expand=True)
        
        close_btn = ctk.CTkButton(
            content_frame,
            text="×",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=BG_DARK,
            text_color=TEXT_WHITE,
            width=16,
            height=16,
            command=lambda: self._remove_toast(toast.id)
        )
        close_btn.pack(side="right", padx=(5, 0))
        
        return toast_frame
    
    def _remove_toast(self, toast_id):
        """Remove a toast"""
        app_state.remove_toast(toast_id)
        # Update visibility after removing toast
        self.after_idle(self.update_toasts)
