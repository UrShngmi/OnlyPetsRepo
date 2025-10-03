"""
Booking page for pet adoption and service booking with multi-step forms
"""
import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from models.app_state import app_state
from models.types import Booking
from utils.colors import *
from views.components.breadcrumbs import Breadcrumbs

class BookingPage(ctk.CTkFrame):
    def __init__(self, parent, app, booking_type, booking_id):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.booking_type = booking_type  # "pet" or "service"
        self.booking_id = booking_id
        
        # Get the item being booked
        if booking_type == "pet":
            self.item = next((p for p in app_state.pets if p.id == booking_id), None)
            self.steps = ["Personal Info", "Adoption Survey", "Review Application", "Confirmation"]
        else:
            self.item = next((s for s in app_state.services if s.id == booking_id), None)
            self.steps = ["Personal Info", "Schedule", "Booking Details", "Review & Confirm", "Confirmation"]
        
        if not self.item:
            self.app.navigate_to("home")
            return
        
        self.current_step = 0
        self.form_data = {
            'name': '', 'email': '', 'phone': '',
            'adoption_reason': '', 'home_environment': '',
            'pet_name': '', 'pet_breed': '', 'special_notes': '',
            'appointment_date': '', 'appointment_time': ''
        }
        
        self.calendar_date = datetime.now()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create booking page widgets"""
        # Title
        title = ctk.CTkLabel(
            self,
            text="Adoption Application" if self.booking_type == "pet" else "Book a Service",
            font=ctk.CTkFont(size=48, weight="bold"),
            text_color=TEXT_WHITE
        )
        title.pack(pady=(0, 5))
        
        if self.current_step < len(self.steps) - 1:
            subtitle = ctk.CTkLabel(
                self,
                text=f"You're applying for: {self.item.name}",
                font=ctk.CTkFont(size=16),
                text_color=TEXT_GRAY_400
            )
            subtitle.pack(pady=(0, 40))
        
        # Container
        self.container = ctk.CTkFrame(self, fg_color=BG_DARK, corner_radius=20)
        self.container.pack(fill="both", expand=True)
        
        # Breadcrumbs
        if self.current_step < len(self.steps) - 1:
            self.breadcrumbs = Breadcrumbs(self.container, self.steps, self.current_step)
            self.breadcrumbs.pack(fill="x", padx=50, pady=(40, 20))
        
        # Form content
        self.form_container = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=50, pady=(0, 40))
        
        self._render_step()
    
    def _render_step(self):
        """Render current step"""
        # Clear form container
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        if self.current_step == len(self.steps) - 1:
            self._render_confirmation()
        else:
            # Form content area
            content_area = ctk.CTkFrame(self.form_container, fg_color="transparent", height=350)
            content_area.pack(fill="both", expand=True, pady=(0, 30))
            
            if self.booking_type == "pet":
                self._render_pet_step(content_area)
            else:
                self._render_service_step(content_area)
            
            # Navigation buttons
            nav_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
            nav_frame.pack(fill="x")
            
            back_btn = ctk.CTkButton(
                nav_frame,
                text="Back",
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=BORDER_GRAY,
                hover_color=HOVER_GRAY,
                text_color=TEXT_WHITE,
                height=50,
                width=150,
                corner_radius=10,
                command=self._go_back,
                state="disabled" if self.current_step == 0 else "normal"
            )
            back_btn.pack(side="left")
            
            next_text = "Confirm & Submit" if self.current_step == len(self.steps) - 2 else "Next Step"
            next_btn = ctk.CTkButton(
                nav_frame,
                text=next_text,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                hover_color=YELLOW_HOVER,
                text_color="black",
                height=50,
                width=150,
                corner_radius=10,
                command=self._go_next
            )
            next_btn.pack(side="right")
    
    def _render_pet_step(self, parent):
        """Render pet adoption steps"""
        if self.current_step == 0:
            self._render_personal_info(parent)
        elif self.current_step == 1:
            self._render_adoption_survey(parent)
        elif self.current_step == 2:
            self._render_pet_review(parent)
    
    def _render_service_step(self, parent):
        """Render service booking steps"""
        if self.current_step == 0:
            self._render_personal_info(parent)
        elif self.current_step == 1:
            self._render_scheduler(parent)
        elif self.current_step == 2:
            self._render_booking_details(parent)
        elif self.current_step == 3:
            self._render_service_review(parent)
    
    def _render_personal_info(self, parent):
        """Render personal info form"""
        title = ctk.CTkLabel(
            parent,
            text="Your Contact Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        self.name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Full Name",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        if self.form_data['name']:
            self.name_entry.insert(0, self.form_data['name'])
        self.name_entry.pack(fill="x", pady=(0, 15))
        
        self.email_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Email Address",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        if self.form_data['email']:
            self.email_entry.insert(0, self.form_data['email'])
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        self.phone_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Phone Number",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        if self.form_data['phone']:
            self.phone_entry.insert(0, self.form_data['phone'])
        self.phone_entry.pack(fill="x")
    
    def _render_adoption_survey(self, parent):
        """Render adoption survey"""
        title = ctk.CTkLabel(
            parent,
            text="Tell Us About Yourself",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        self.adoption_reason_text = ctk.CTkTextbox(
            parent,
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=100
        )
        
        # Set up placeholder behavior
        self.adoption_placeholder = "Why are you looking to adopt a pet at this time? (e.g., companionship, family pet, first-time owner)"
        self.adoption_has_placeholder = True
        
        if self.form_data['adoption_reason']:
            self.adoption_reason_text.insert("1.0", self.form_data['adoption_reason'])
            self.adoption_has_placeholder = False
        else:
            # Insert placeholder text immediately on load
            self.adoption_reason_text.insert("1.0", self.adoption_placeholder)
            self.adoption_reason_text.configure(text_color=TEXT_GRAY_500)
        
        # Bind events for placeholder behavior
        self.adoption_reason_text.bind("<FocusIn>", self._on_adoption_focus_in)
        self.adoption_reason_text.bind("<FocusOut>", self._on_adoption_focus_out)
        self.adoption_reason_text.pack(fill="x", pady=(0, 15))
        
        self.home_env_text = ctk.CTkTextbox(
            parent,
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=100
        )
        
        # Set up placeholder behavior
        self.home_placeholder = "Describe your home environment (e.g., apartment, house with yard, other pets, children)"
        self.home_has_placeholder = True
        
        if self.form_data['home_environment']:
            self.home_env_text.insert("1.0", self.form_data['home_environment'])
            self.home_has_placeholder = False
        else:
            # Insert placeholder text immediately on load
            self.home_env_text.insert("1.0", self.home_placeholder)
            self.home_env_text.configure(text_color=TEXT_GRAY_500)
        
        # Bind events for placeholder behavior
        self.home_env_text.bind("<FocusIn>", self._on_home_focus_in)
        self.home_env_text.bind("<FocusOut>", self._on_home_focus_out)
        self.home_env_text.pack(fill="x")
    
    def _render_scheduler(self, parent):
        """Render calendar scheduler"""
        # Calendar
        cal_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cal_frame.pack(fill="both", expand=True)
        
        # Month navigation
        nav_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
        nav_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkButton(
            nav_frame,
            text="<",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_WHITE,
            width=40,
            command=self._prev_month
        ).pack(side="left")
        
        month_label = ctk.CTkLabel(
            nav_frame,
            text=self.calendar_date.strftime("%B %Y"),
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_WHITE
        )
        month_label.pack(side="left", expand=True)
        
        ctk.CTkButton(
            nav_frame,
            text=">",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            hover_color=HOVER_GRAY,
            text_color=TEXT_WHITE,
            width=40,
            command=self._next_month
        ).pack(side="right")
        
        # Calendar grid
        cal_grid = ctk.CTkFrame(cal_frame, fg_color="transparent")
        cal_grid.pack()
        
        # Days of week
        days = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        for i, day in enumerate(days):
            ctk.CTkLabel(
                cal_grid,
                text=day,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TEXT_GRAY_500,
                width=40,
                height=40
            ).grid(row=0, column=i, padx=2, pady=2)
        
        # Calendar days
        year = self.calendar_date.year
        month = self.calendar_date.month
        first_day = calendar.monthrange(year, month)[0]
        days_in_month = calendar.monthrange(year, month)[1]
        
        day_num = 1
        for week in range(6):
            for day_col in range(7):
                if week == 0 and day_col < first_day:
                    continue
                if day_num > days_in_month:
                    break
                
                date_obj = datetime(year, month, day_num)
                is_past = date_obj.date() < datetime.now().date()
                date_str = date_obj.strftime('%Y-%m-%d')
                is_selected = self.form_data['appointment_date'] == date_str
                
                btn = ctk.CTkButton(
                    cal_grid,
                    text=str(day_num),
                    font=ctk.CTkFont(size=14, weight="bold" if is_selected else "normal"),
                    fg_color=YELLOW_PRIMARY if is_selected else ("transparent" if not is_past else BG_DARK),
                    hover_color=YELLOW_HOVER if not is_past else BG_DARK,
                    text_color="black" if is_selected else (TEXT_GRAY_600 if is_past else TEXT_WHITE),
                    width=40,
                    height=40,
                    corner_radius=20,
                    state="disabled" if is_past else "normal",
                    command=lambda d=date_str: self._select_date(d)
                )
                btn.grid(row=week+1, column=day_col, padx=2, pady=2)
                
                day_num += 1
        
        # Time slot selection
        if self.form_data['appointment_date']:
            time_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
            time_frame.pack(fill="x", pady=(20, 0))
            
            ctk.CTkLabel(
                time_frame,
                text=f"Select a Time Slot for {self.form_data['appointment_date']}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=TEXT_WHITE
            ).pack(pady=(0, 15))
            
            slots_grid = ctk.CTkFrame(time_frame, fg_color="transparent")
            slots_grid.pack()
            
            slots_grid.grid_columnconfigure((0, 1), weight=1)
            
            slots = [
                ('morning', 'Morning', '9:00 AM - 12:00 PM'),
                ('afternoon', 'Afternoon', '1:00 PM - 5:00 PM')
            ]
            
            for i, (slot_id, slot_name, slot_time) in enumerate(slots):
                is_booked = app_state.is_slot_booked(self.booking_id, self.form_data['appointment_date'], slot_id)
                is_selected = self.form_data['appointment_time'] == slot_id
                
                btn = ctk.CTkButton(
                    slots_grid,
                    text=f"{slot_name}\n{slot_time}",
                    font=ctk.CTkFont(size=14, weight="bold" if is_selected else "normal"),
                    fg_color=YELLOW_PRIMARY if is_selected else BG_SECONDARY,
                    hover_color=YELLOW_HOVER if not is_booked else BG_SECONDARY,
                    text_color="black" if is_selected else (TEXT_GRAY_600 if is_booked else TEXT_WHITE),
                    height=70,
                    corner_radius=10,
                    border_width=2,
                    border_color=YELLOW_PRIMARY if is_selected else (BORDER_GRAY if not is_booked else RED_ERROR),
                    state="disabled" if is_booked else "normal",
                    command=lambda s=slot_id: self._select_time_slot(s)
                )
                btn.grid(row=0, column=i, padx=10, sticky="ew")
                
                if is_booked:
                    ctk.CTkLabel(
                        slots_grid,
                        text="Unavailable",
                        font=ctk.CTkFont(size=11),
                        text_color=RED_ERROR
                    ).grid(row=1, column=i, pady=(5, 0))
    
    def _render_booking_details(self, parent):
        """Render booking details form"""
        title = ctk.CTkLabel(
            parent,
            text="Tell Us About Your Pet",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        self.pet_name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Pet's Name",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        if self.form_data['pet_name']:
            self.pet_name_entry.insert(0, self.form_data['pet_name'])
        self.pet_name_entry.pack(fill="x", pady=(0, 15))
        
        self.pet_breed_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Pet's Breed",
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=45
        )
        if self.form_data['pet_breed']:
            self.pet_breed_entry.insert(0, self.form_data['pet_breed'])
        self.pet_breed_entry.pack(fill="x", pady=(0, 15))
        
        self.special_notes_text = ctk.CTkTextbox(
            parent,
            font=ctk.CTkFont(size=14),
            fg_color=BG_SECONDARY,
            border_color=BORDER_GRAY,
            height=100
        )
        
        # Set up placeholder behavior
        self.notes_placeholder = "Any special notes or instructions for our staff? (e.g., allergies, behavior quirks, special care needed)"
        self.notes_has_placeholder = True
        
        if self.form_data['special_notes']:
            self.special_notes_text.insert("1.0", self.form_data['special_notes'])
            self.notes_has_placeholder = False
        else:
            # Insert placeholder text immediately on load
            self.special_notes_text.insert("1.0", self.notes_placeholder)
            self.special_notes_text.configure(text_color=TEXT_GRAY_500)
        
        # Bind events for placeholder behavior
        self.special_notes_text.bind("<FocusIn>", self._on_notes_focus_in)
        self.special_notes_text.bind("<FocusOut>", self._on_notes_focus_out)
        self.special_notes_text.pack(fill="x")
    
    def _render_pet_review(self, parent):
        """Render adoption review"""
        review_frame = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=15)
        review_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        content = ctk.CTkFrame(review_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            content,
            text="Confirm Your Details",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        details = [
            ("Applying to Adopt:", self.item.name),
            ("Name:", self.form_data['name']),
            ("Email:", self.form_data['email']),
            ("Phone:", self.form_data['phone']),
            ("Reason for Adopting:", self.form_data['adoption_reason'] or 'N/A'),
            ("Home Environment:", self.form_data['home_environment'] or 'N/A')
        ]
        
        for i, (label, value) in enumerate(details):
            if i == 1:
                ctk.CTkFrame(content, fg_color=BORDER_GRAY, height=1).pack(fill="x", pady=10)
            if i == 4:
                ctk.CTkFrame(content, fg_color=BORDER_GRAY, height=1).pack(fill="x", pady=10)
            
            row = ctk.CTkFrame(content, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_GRAY_300,
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_WHITE,
                anchor="w",
                wraplength=600
            ).pack(fill="x", padx=(20, 0))
    
    def _render_service_review(self, parent):
        """Render service booking review"""
        review_frame = ctk.CTkFrame(parent, fg_color=BG_SECONDARY, corner_radius=15)
        review_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        content = ctk.CTkFrame(review_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=30)
        
        title = ctk.CTkLabel(
            content,
            text="Confirm Your Booking",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_WHITE,
            anchor="w"
        )
        title.pack(fill="x", pady=(0, 20))
        
        time_slot_text = "Morning" if self.form_data['appointment_time'] == 'morning' else "Afternoon"
        
        details = [
            ("Service:", self.item.name),
            ("Appointment:", f"{self.form_data['appointment_date']} ({time_slot_text})"),
            ("Your Name:", self.form_data['name']),
            ("Contact:", self.form_data['email']),
            ("Pet Name:", self.form_data['pet_name']),
            ("Pet Breed:", self.form_data['pet_breed']),
            ("Notes:", self.form_data['special_notes'] or 'None')
        ]
        
        for i, (label, value) in enumerate(details):
            if i == 2 or i == 4:
                ctk.CTkFrame(content, fg_color=BORDER_GRAY, height=1).pack(fill="x", pady=10)
            
            row = ctk.CTkFrame(content, fg_color="transparent")
            row.pack(fill="x", pady=5)
            
            ctk.CTkLabel(
                row,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_GRAY_300,
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                row,
                text=value,
                font=ctk.CTkFont(size=14),
                text_color=TEXT_WHITE,
                anchor="w",
                wraplength=600
            ).pack(fill="x", padx=(20, 0))
    
    def _render_confirmation(self):
        """Render confirmation screen"""
        # Clear form container
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        # Create centered content frame with proper grid
        confirm_frame = ctk.CTkFrame(self.form_container, fg_color="transparent")
        confirm_frame.pack(expand=True, fill="both")
        
        # Configure grid for centering
        confirm_frame.grid_rowconfigure(0, weight=1)
        confirm_frame.grid_columnconfigure(0, weight=1)
        
        # Center content using grid
        center_frame = ctk.CTkFrame(confirm_frame, fg_color="transparent")
        center_frame.grid(row=0, column=0, sticky="")
        
        # Large green check icon with green background
        icon_frame = ctk.CTkLabel(
            center_frame,
            text="✓",
            font=ctk.CTkFont(size=64, weight="bold"),
            fg_color="#22c55e",  # Green background
            text_color="white",
            width=120,
            height=120,
            corner_radius=60
        )
        icon_frame.pack(pady=(0, 30))
        
        if self.booking_type == "pet":
            # Pet adoption confirmation
            title = ctk.CTkLabel(
                center_frame,
                text="Application Submitted!",
                font=ctk.CTkFont(size=36, weight="bold"),
                text_color=TEXT_WHITE
            )
            title.pack(pady=(0, 20))
            
            message = f"Thank you for your interest in adopting {self.item.name}.\nWe have received your application and will contact you\nwithin 3-5 business days to discuss the next steps."
            
            msg_label = ctk.CTkLabel(
                center_frame,
                text=message,
                font=ctk.CTkFont(size=16),
                text_color=TEXT_GRAY_300,
                justify="center"
            )
            msg_label.pack(pady=(0, 40))
            
            # Back to Homepage button
            home_btn = ctk.CTkButton(
                center_frame,
                text="Back to Homepage",
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                hover_color=YELLOW_HOVER,
                text_color="black",
                height=50,
                width=200,
                corner_radius=10,
                command=lambda: self.app.navigate_to("home")
            )
            home_btn.pack()
        else:
            # Service booking confirmation
            title = ctk.CTkLabel(
                center_frame,
                text="Booking Confirmed!",
                font=ctk.CTkFont(size=36, weight="bold"),
                text_color=TEXT_WHITE
            )
            title.pack(pady=(0, 20))
            
            # Format the appointment details properly
            appointment_date = self.form_data.get('appointment_date', '')
            appointment_time = self.form_data.get('appointment_time', '')
            time_display = "Morning (9:00 AM - 12:00 PM)" if appointment_time == 'morning' else "Afternoon (1:00 PM - 5:00 PM)"
            pet_name = self.form_data.get('pet_name', 'your pet')
            
            message = f"Your appointment for {self.item.name} on {appointment_date}\n({time_display}) is confirmed.\nWe look forward to seeing you and {pet_name}!"
            
            msg_label = ctk.CTkLabel(
                center_frame,
                text=message,
                font=ctk.CTkFont(size=16),
                text_color=TEXT_GRAY_300,
                justify="center"
            )
            msg_label.pack(pady=(0, 40))
            
            # Back to Homepage button
            home_btn = ctk.CTkButton(
                center_frame,
                text="Back to Homepage",
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=YELLOW_PRIMARY,
                hover_color=YELLOW_HOVER,
                text_color="black",
                height=50,
                width=200,
                corner_radius=10,
                command=lambda: self.app.navigate_to("home")
            )
            home_btn.pack()
    
    def _save_current_step(self):
        """Save current step data"""
        if self.current_step == 0:
            self.form_data['name'] = self.name_entry.get().strip()
            self.form_data['email'] = self.email_entry.get().strip()
            self.form_data['phone'] = self.phone_entry.get().strip()
        elif self.current_step == 1 and self.booking_type == "pet":
            adoption_text = self.adoption_reason_text.get("1.0", "end-1c").strip()
            home_text = self.home_env_text.get("1.0", "end-1c").strip()
            
            # Filter out placeholder text if it's still showing
            if hasattr(self, 'adoption_has_placeholder') and self.adoption_has_placeholder:
                adoption_text = ""
            if hasattr(self, 'home_has_placeholder') and self.home_has_placeholder:
                home_text = ""
                
            self.form_data['adoption_reason'] = adoption_text
            self.form_data['home_environment'] = home_text
        elif self.current_step == 2 and self.booking_type == "service":
            self.form_data['pet_name'] = self.pet_name_entry.get().strip()
            self.form_data['pet_breed'] = self.pet_breed_entry.get().strip()
            
            special_notes_text = self.special_notes_text.get("1.0", "end-1c").strip()
            # Filter out placeholder text if it's still showing
            if hasattr(self, 'notes_has_placeholder') and self.notes_has_placeholder:
                special_notes_text = ""
            self.form_data['special_notes'] = special_notes_text
    
    def _validate_current_step(self):
        """Validate current step"""
        if self.current_step == 0:
            # Validate personal info
            if not self.form_data['name']:
                app_state.add_toast("Please enter your full name.", "error")
                return False
            
            if len(self.form_data['name']) < 2:
                app_state.add_toast("Please enter a valid full name (at least 2 characters).", "error")
                return False
            
            if not self.form_data['email']:
                app_state.add_toast("Please enter your email address.", "error")
                return False
            
            if "@" not in self.form_data['email'] or "." not in self.form_data['email'].split("@")[-1]:
                app_state.add_toast("Please enter a valid email address.", "error")
                return False
            
            if not self.form_data['phone']:
                app_state.add_toast("Please enter your phone number.", "error")
                return False
            
            # Basic phone validation (digits, spaces, dashes, parentheses)
            phone_clean = ''.join(c for c in self.form_data['phone'] if c.isdigit())
            if len(phone_clean) < 10:
                app_state.add_toast("Please enter a valid phone number (at least 10 digits).", "error")
                return False
                
        elif self.current_step == 1:
            if self.booking_type == "pet":
                if not self.form_data['adoption_reason']:
                    app_state.add_toast("Please tell us why you want to adopt this pet.", "error")
                    return False
                
                if len(self.form_data['adoption_reason']) < 20:
                    app_state.add_toast("Please provide more details about your adoption reason (at least 20 characters).", "error")
                    return False
                
                if not self.form_data['home_environment']:
                    app_state.add_toast("Please describe your home environment.", "error")
                    return False
                
                if len(self.form_data['home_environment']) < 20:
                    app_state.add_toast("Please provide more details about your home environment (at least 20 characters).", "error")
                    return False
            else:
                if not self.form_data['appointment_date']:
                    app_state.add_toast("Please select an appointment date.", "error")
                    return False
                
                if not self.form_data['appointment_time']:
                    app_state.add_toast("Please select an appointment time.", "error")
                    return False
                    
        elif self.current_step == 2 and self.booking_type == "service":
            if not self.form_data['pet_name']:
                app_state.add_toast("Please enter your pet's name.", "error")
                return False
            
            if len(self.form_data['pet_name']) < 2:
                app_state.add_toast("Please enter a valid pet name (at least 2 characters).", "error")
                return False
            
            if not self.form_data['pet_breed']:
                app_state.add_toast("Please enter your pet's breed.", "error")
                return False
            
            if len(self.form_data['pet_breed']) < 2:
                app_state.add_toast("Please enter a valid pet breed (at least 2 characters).", "error")
                return False
                
        return True
    
    def _go_back(self):
        """Go to previous step"""
        if self.current_step > 0:
            self._save_current_step()
            self.current_step -= 1
            # Update breadcrumbs
            if hasattr(self, 'breadcrumbs'):
                self.breadcrumbs.update_step(self.current_step)
            self._render_step()
    
    def _go_next(self):
        """Go to next step"""
        self._save_current_step()
        
        if not self._validate_current_step():
            return
        
        if self.current_step == len(self.steps) - 2:
            # Submit
            if self.booking_type == "service":
                from datetime import datetime
                booking = Booking(
                    id=str(int(datetime.now().timestamp())),
                    service_id=self.booking_id,
                    date=self.form_data['appointment_date'],
                    time_slot=self.form_data['appointment_time'],
                    user_id=app_state.current_user.id if app_state.current_user else "",
                    status="confirmed"
                )
                app_state.add_booking(booking)
                # Add success toast notification
                app_state.add_toast(f"Service booking confirmed! Your {self.item.name} appointment is scheduled.", "success")
            else:
                # Pet adoption submission
                app_state.add_toast(f"Adoption application submitted! We'll contact you about {self.item.name} soon.", "success")
        
        self.current_step += 1
        # Update breadcrumbs
        if hasattr(self, 'breadcrumbs'):
            self.breadcrumbs.update_step(self.current_step)
        self._render_step()
    
    def _prev_month(self):
        """Go to previous month"""
        self.calendar_date = self.calendar_date.replace(day=1) - timedelta(days=1)
        self._render_step()
    
    def _next_month(self):
        """Go to next month"""
        next_month = self.calendar_date.month + 1
        next_year = self.calendar_date.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        self.calendar_date = self.calendar_date.replace(year=next_year, month=next_month, day=1)
        self._render_step()
    
    def _select_date(self, date_str):
        """Select appointment date"""
        self.form_data['appointment_date'] = date_str
        self.form_data['appointment_time'] = ''
        self._render_step()
    
    def _select_time_slot(self, slot):
        """Select time slot"""
        self.form_data['appointment_time'] = slot
        self._render_step()
    
    def _on_adoption_focus_in(self, event):
        """Handle adoption textbox focus in"""
        if hasattr(self, 'adoption_has_placeholder') and self.adoption_has_placeholder:
            self.adoption_reason_text.delete("1.0", "end")
            self.adoption_reason_text.configure(text_color=TEXT_WHITE)
            self.adoption_has_placeholder = False
    
    def _on_adoption_focus_out(self, event):
        """Handle adoption textbox focus out"""
        if hasattr(self, 'adoption_reason_text'):
            content = self.adoption_reason_text.get("1.0", "end-1c").strip()
            if not content:
                self.adoption_reason_text.insert("1.0", self.adoption_placeholder)
                self.adoption_reason_text.configure(text_color=TEXT_GRAY_500)
                self.adoption_has_placeholder = True
    
    def _on_home_focus_in(self, event):
        """Handle home environment textbox focus in"""
        if hasattr(self, 'home_has_placeholder') and self.home_has_placeholder:
            self.home_env_text.delete("1.0", "end")
            self.home_env_text.configure(text_color=TEXT_WHITE)
            self.home_has_placeholder = False
    
    def _on_home_focus_out(self, event):
        """Handle home environment textbox focus out"""
        if hasattr(self, 'home_env_text'):
            content = self.home_env_text.get("1.0", "end-1c").strip()
            if not content:
                self.home_env_text.insert("1.0", self.home_placeholder)
                self.home_env_text.configure(text_color=TEXT_GRAY_500)
                self.home_has_placeholder = True
    
    def _on_notes_focus_in(self, event):
        """Handle special notes textbox focus in"""
        if hasattr(self, 'notes_has_placeholder') and self.notes_has_placeholder:
            self.special_notes_text.delete("1.0", "end")
            self.special_notes_text.configure(text_color=TEXT_WHITE)
            self.notes_has_placeholder = False
    
    def _on_notes_focus_out(self, event):
        """Handle special notes textbox focus out"""
        if hasattr(self, 'special_notes_text'):
            content = self.special_notes_text.get("1.0", "end-1c").strip()
            if not content:
                self.special_notes_text.insert("1.0", self.notes_placeholder)
                self.special_notes_text.configure(text_color=TEXT_GRAY_500)
                self.notes_has_placeholder = True
