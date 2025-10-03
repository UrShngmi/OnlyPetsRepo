"""
Manage Bookings page for viewing and canceling existing bookings
"""
import customtkinter as ctk
from models.app_state import app_state
from utils.colors import *

class ManageBookingsPage(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self._create_widgets()
    
    def _create_widgets(self):
        """Create manage bookings page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Manage Your Bookings",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        subtitle = ctk.CTkLabel(
            self,
            text="View and manage your service appointments",
            font=ctk.CTkFont(size=16),
            text_color=TEXT_GRAY_400
        )
        subtitle.pack(pady=(0, 40))
        
        # Main container
        main_container = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=20)
        main_container.pack(fill="both", expand=True, padx=40, pady=(0, 40))
        
        # Content area
        content_frame = ctk.CTkScrollableFrame(main_container, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Check if user has bookings
        user_bookings = app_state.get_user_bookings()
        
        if not user_bookings:
            # No bookings message
            no_bookings_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            no_bookings_frame.pack(expand=True)
            
            icon = ctk.CTkLabel(
                no_bookings_frame,
                text="📅",
                font=ctk.CTkFont(size=48),
                text_color=TEXT_GRAY_500
            )
            icon.pack(pady=(50, 20))
            
            no_bookings_label = ctk.CTkLabel(
                no_bookings_frame,
                text="No Bookings Yet",
                font=ctk.CTkFont(size=24, weight="bold"),
                text_color=TEXT_WHITE
            )
            no_bookings_label.pack(pady=(0, 10))
            
            desc_label = ctk.CTkLabel(
                no_bookings_frame,
                text="You haven't made any service bookings yet. Book a service to see your appointments here.",
                font=ctk.CTkFont(size=14),
                text_color=TEXT_GRAY_400,
                wraplength=400,
                justify="center"
            )
            desc_label.pack(pady=(0, 30))
            
            # Book service button
            book_btn = ctk.CTkButton(
                no_bookings_frame,
                text="Book a Service",
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                hover_color=YELLOW_HOVER,
                text_color="black",
                height=50,
                width=200,
                corner_radius=10,
                command=lambda: self.app.navigate_to("services")
            )
            book_btn.pack()
        else:
            # Display bookings
            for booking in user_bookings:
                self._create_booking_card(content_frame, booking)
    
    def _create_booking_card(self, parent, booking):
        """Create a booking card"""
        # Get service details
        service = next((s for s in app_state.services if s.id == booking.service_id), None)
        if not service:
            return
        
        card = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=15)
        card.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Header row
        header_frame = ctk.CTkFrame(content, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 15))
        
        # Service name
        service_name = ctk.CTkLabel(
            header_frame,
            text=service.name,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        service_name.pack(side="left")
        
        # Status badge
        status_color = GREEN_SUCCESS if booking.status == "confirmed" else TEXT_GRAY_500
        status_badge = ctk.CTkLabel(
            header_frame,
            text=booking.status.upper(),
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=status_color,
            text_color="white",
            corner_radius=12,
            width=80,
            height=24
        )
        status_badge.pack(side="right")
        
        # Details row
        details_frame = ctk.CTkFrame(content, fg_color="transparent")
        details_frame.pack(fill="x", pady=(0, 15))
        
        # Date and time
        datetime_label = ctk.CTkLabel(
            details_frame,
            text=f"📅 {booking.date} at {booking.time_slot}",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300,
            anchor="w"
        )
        datetime_label.pack(side="left")
        
        # Price
        price_label = ctk.CTkLabel(
            details_frame,
            text=f"₱{service.price:.2f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=YELLOW_PRIMARY,
            anchor="e"
        )
        price_label.pack(side="right")
        
        # Actions row
        actions_frame = ctk.CTkFrame(content, fg_color="transparent")
        actions_frame.pack(fill="x")
        
        # Cancel button (only if confirmed)
        if booking.status == "confirmed":
            cancel_btn = ctk.CTkButton(
                actions_frame,
                text="Cancel Booking",
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="transparent",
                hover_color="#7f1d1d",
                text_color="#ef4444",
                border_width=2,
                border_color="#ef4444",
                height=35,
                width=120,
                corner_radius=8,
                command=lambda b=booking: self._cancel_booking(b)
            )
            cancel_btn.pack(side="right")
        
    
    def _cancel_booking(self, booking):
        """Cancel a booking with confirmation modal"""
        self._show_cancel_confirmation_modal(booking)
    
    def _show_cancel_confirmation_modal(self, booking):
        """Show centered confirmation modal for booking cancellation"""
        # Create modal overlay
        self.modal_overlay = ctk.CTkFrame(
            self.winfo_toplevel(),
            fg_color=("gray75", "gray25"),
            corner_radius=0
        )
        self.modal_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Create modal dialog
        modal_dialog = ctk.CTkFrame(
            self.modal_overlay,
            fg_color=BG_DARK,
            corner_radius=20,
            border_width=2,
            border_color=BORDER_GRAY,
            width=400,
            height=250
        )
        modal_dialog.place(relx=0.5, rely=0.5, anchor="center")
        
        # Modal content
        content_frame = ctk.CTkFrame(modal_dialog, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Warning icon
        warning_icon = ctk.CTkLabel(
            content_frame,
            text="⚠️",
            font=ctk.CTkFont(size=32),
            text_color=YELLOW_PRIMARY
        )
        warning_icon.pack(pady=(0, 15))
        
        # Title
        title_label = ctk.CTkLabel(
            content_frame,
            text="Cancel Booking",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE
        )
        title_label.pack(pady=(0, 10))
        
        # Message
        service = next((s for s in app_state.services if s.id == booking.service_id), None)
        service_name = service.name if service else "this service"
        
        message_label = ctk.CTkLabel(
            content_frame,
            text=f"Are you sure you want to cancel your\n{service_name} booking?",
            font=ctk.CTkFont(size=14),
            text_color=TEXT_GRAY_300,
            justify="center"
        )
        message_label.pack(pady=(0, 25))
        
        # Buttons
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x")
        
        # Cancel button (keep booking)
        keep_btn = ctk.CTkButton(
            button_frame,
            text="Keep Booking",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_WHITE,
            border_width=2,
            border_color=BORDER_GRAY,
            height=40,
            width=120,
            corner_radius=8,
            command=self._close_cancel_modal
        )
        keep_btn.pack(side="left")
        
        # Confirm cancel button
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="Cancel Booking",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="white",
            height=40,
            width=120,
            corner_radius=8,
            command=lambda: self._confirm_cancel_booking(booking)
        )
        confirm_btn.pack(side="right")
        
        # Bind escape key to close
        self.winfo_toplevel().bind("<Escape>", lambda e: self._close_cancel_modal())
        
        # Focus the modal
        modal_dialog.focus_set()
    
    def _close_cancel_modal(self):
        """Close the cancellation modal"""
        if hasattr(self, 'modal_overlay') and self.modal_overlay.winfo_exists():
            self.modal_overlay.destroy()
        self.winfo_toplevel().unbind("<Escape>")
    
    def _confirm_cancel_booking(self, booking):
        """Confirm and execute booking cancellation"""
        app_state.cancel_booking(booking.id)
        app_state.add_toast("Booking cancelled successfully.", "success")
        self._close_cancel_modal()
        # Refresh the page
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets()
    
