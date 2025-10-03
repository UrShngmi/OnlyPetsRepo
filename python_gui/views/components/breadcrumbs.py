"""
Breadcrumbs component for multi-step workflows
"""
import customtkinter as ctk
from utils.colors import *

class Breadcrumbs(ctk.CTkFrame):
    def __init__(self, parent, steps, current_step):
        super().__init__(parent, fg_color="transparent")
        self.steps = steps
        self.current_step = current_step
        self.container = None
        self._create_widgets()
    
    def update_step(self, new_step):
        """Update the current step and refresh the breadcrumbs"""
        self.current_step = new_step
        self._refresh_widgets()
    
    def _create_widgets(self):
        """Create breadcrumb widgets"""
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="x", pady=20)
        
        # Center the breadcrumbs
        breadcrumb_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        breadcrumb_frame.pack(expand=True)
        
        self._build_breadcrumbs(breadcrumb_frame)
    
    def _refresh_widgets(self):
        """Refresh breadcrumb widgets"""
        # Clear existing widgets
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Recreate breadcrumbs
        breadcrumb_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        breadcrumb_frame.pack(expand=True)
        
        self._build_breadcrumbs(breadcrumb_frame)
    
    def _build_breadcrumbs(self, parent_frame):
        """Build the breadcrumb elements"""
        num_steps = len(self.steps)
        
        for i, step in enumerate(self.steps):
            # Step container
            step_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            step_frame.pack(side="left", padx=10)
            
            is_completed = i < self.current_step
            is_current = i == self.current_step
            
            # Circle
            if is_completed:
                circle = ctk.CTkLabel(
                    step_frame,
                    text="✓",
                    font=ctk.CTkFont(size=18, weight="bold"),
                    fg_color=YELLOW_PRIMARY,
                    text_color="black",
                    width=50,
                    height=50,
                    corner_radius=25
                )
                circle.pack()
            else:
                circle_color = YELLOW_PRIMARY if is_current else BORDER_GRAY
                text_color = "black" if is_current else TEXT_GRAY_500
                
                # Create circle frame with border
                circle_frame = ctk.CTkFrame(
                    step_frame,
                    width=50,
                    height=50,
                    corner_radius=25,
                    fg_color=circle_color if is_current else "transparent",
                    border_width=3,
                    border_color=circle_color
                )
                circle_frame.pack_propagate(False)
                circle_frame.pack()
                
                circle = ctk.CTkLabel(
                    circle_frame,
                    text=f"{i+1}",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    fg_color="transparent",
                    text_color=text_color
                )
                circle.pack(expand=True)
            
            # Step label
            label_text = step.replace(' ', '\n') if len(step) > 15 else step
            label = ctk.CTkLabel(
                step_frame,
                text=label_text,
                font=ctk.CTkFont(size=13, weight="bold" if is_current or is_completed else "normal"),
                text_color=YELLOW_PRIMARY if (is_current or is_completed) else TEXT_GRAY_500,
                width=100,
                justify="center"
            )
            label.pack(pady=(8, 0))
            
            # Connector line (centered between circles)
            if i < num_steps - 1:
                connector = ctk.CTkFrame(
                    parent_frame,
                    fg_color=YELLOW_PRIMARY if is_completed else BORDER_GRAY,
                    height=3,
                    width=60
                )
                connector.pack(side="left", padx=15, pady=(25, 0), anchor="center")
