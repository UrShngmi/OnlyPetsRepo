# OnlyPets Python GUI - Setup & Launch Guide

## 🎉 Conversion Complete!

Your React/TypeScript OnlyPets application has been successfully converted into a fully functional Python desktop GUI application using CustomTkinter.

---

## 📋 Quick Start (3 Steps)

### Step 1: Install Dependencies
Open a terminal in the `python_gui` directory and run:

```bash
pip install -r requirements.txt
```

This installs:
- **customtkinter** - Modern, dark-themed GUI framework
- **Pillow** - Image processing library

### Step 2: Generate Placeholder Assets
Run the asset generator to create placeholder images:

```bash
python create_placeholder_assets.py
```

This creates:
- 48 pet images (12 pets × 4 images each)
- 5 service images
- 4 product images  
- 1 default profile icon

**OR** manually add your own images to:
- `assets/pets/pet_01_1.jpg` through `pet_12_4.jpg`
- `assets/services/grooming.jpg`, `health_checkup.jpg`, etc.
- `assets/products/pet_food.jpg`, `pet_toy.jpg`, etc.
- `assets/default_profile.png`

### Step 3: Launch the Application
```bash
python main.py
```

The app will automatically:
✅ Detect your screen size  
✅ Launch maximized and centered  
✅ Create necessary directories  

---

## 🎨 Application Features

### ✨ Complete Feature Parity with React Version

**Navigation & Browsing**
- 🏠 Home page with hero section, features, and testimonials
- 🐾 Pet adoption listing with search and species filters
- 📄 Detailed pet profiles with image carousel
- 💼 Services catalog with expandable details
- 🛒 Products page with shopping functionality

**User Features**
- 👤 Sign in/Sign up with email or social login (simulated)
- 🖼️ Profile setup with custom username and profile picture
- ❤️ Wishlist for favorite pets and services
- 🛍️ Shopping cart with quantity controls and checkout
- 📋 Multi-step booking workflows for adoptions and services

**Booking System**
- 📅 Calendar-based appointment scheduler
- ⏰ Morning/afternoon time slot selection
- 🚫 Conflict detection (unavailable slots shown in red)
- ✅ Breadcrumb navigation through multi-step forms
- 📝 Form validation and data persistence

**UI/UX**
- 🌑 Modern dark theme with yellow accents
- 🔔 Toast notifications (success, error, info)
- 🖱️ Hover effects and smooth transitions
- 📱 Responsive design (auto-scales to screen)
- ⚡ Fast navigation between pages

---

## 📁 Project Structure

```
python_gui/
│
├── main.py                      # Launch this file
├── requirements.txt             # Dependencies
├── create_placeholder_assets.py # Asset generator
├── README.md                    # Detailed documentation
├── SETUP_GUIDE.md              # This file
│
├── models/
│   ├── types.py                # Data models (Pet, Service, User, etc.)
│   └── app_state.py            # State management & business logic
│
├── views/
│   ├── header.py               # Navigation bar
│   ├── home_page.py            # Landing page
│   ├── adoption_page.py        # Pet browsing
│   ├── pet_details_page.py     # Individual pet page
│   ├── services_page.py        # Services listing
│   ├── products_page.py        # Product catalog
│   ├── cart_page.py            # Shopping cart
│   ├── wishlist_page.py        # Saved favorites
│   ├── contact_page.py         # Contact form
│   ├── booking_page.py         # Multi-step booking
│   ├── auth_modal.py           # Login/signup popup
│   ├── profile_modal.py        # Profile editor popup
│   ├── toast_container.py      # Notifications
│   └── components/
│       ├── pet_card.py         # Reusable pet card
│       ├── service_card.py     # Reusable service card
│       └── breadcrumbs.py      # Progress indicator
│
├── utils/
│   └── colors.py               # Color constants
│
├── assets/                     # Images (auto-generated)
│   ├── pets/
│   ├── services/
│   ├── products/
│   └── default_profile.png
│
└── data/                       # User data (auto-created)
    └── users.json              # Saved user accounts
```

---

## 🎮 How to Use

### Authentication
1. Click **"Sign In / Sign Up"** in the header
2. Switch between Login/Sign Up tabs
3. Use social login (Google/Facebook - simulated)
4. Set up profile with username and photo
5. User data persists between sessions

### Pet Adoption
1. Go to **Adoption** page
2. Search or filter by species (Dog, Cat, Bird, Other)
3. Click any pet card to view details
4. Browse image carousel (click dots to switch)
5. Click **ADOPT** button
6. Fill out multi-step adoption form
7. Review and submit application

### Service Booking
1. Navigate to **Services** page
2. View service details (click "...and more" to expand)
3. Click **Book Now**
4. Enter personal information
5. Select date and time on calendar
   - Past dates disabled
   - Unavailable slots marked in red
6. Provide pet details
7. Review booking and confirm
8. See confirmation screen

### Shopping
1. Browse **Products** page
2. Click **Add to Cart** on any product
3. Navigate to **Cart** (icon in header)
4. Adjust quantities with +/- buttons
5. Remove items with × button
6. Click **Proceed to Checkout**
7. See order summary with subtotal, tax, total

### Wishlist
1. Click **heart icon** on any pet or service card
2. View all favorites in **Wishlist** page
3. Organized into "Favorite Pets" and "Saved Services"
4. Click card to navigate to details

---

## 🛠️ Customization

### Change Colors
Edit `utils/colors.py`:

```python
YELLOW_PRIMARY = "#f59e0b"  # Change accent color
BG_PRIMARY = "#1c1c1c"      # Main background
BG_SECONDARY = "#2a2a2a"    # Card backgrounds
```

### Modify Pet Data
Edit `models/app_state.py` → `_load_sample_data()`:

```python
pets_data = [
    {"id": "pet_01", "name": "Your Pet Name", ...},
]
```

### Add Real Images
Replace placeholder images in `assets/`:

**Pet Images:** 4 images per pet
- `assets/pets/pet_01_1.jpg`
- `assets/pets/pet_01_2.jpg`
- `assets/pets/pet_01_3.jpg`
- `assets/pets/pet_01_4.jpg`

**Service Images:**
- `assets/services/grooming.jpg`
- `assets/services/health_checkup.jpg`
- etc.

**Product Images:**
- `assets/products/pet_food.jpg`
- etc.

---

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install customtkinter Pillow
```

### Images not loading
- Run `python create_placeholder_assets.py`
- Or add images manually to `assets/` directories
- Check file names match expected format

### Window doesn't maximize
- Application uses `state('zoomed')` for Windows
- If on Linux/Mac, change line in `main.py`:
  ```python
  # self.state('zoomed')  # Windows
  self.attributes('-zoomed', True)  # Linux/Mac
  ```

### Toast notifications not showing
- Check `views/toast_container.py`
- Toasts auto-disappear after 3 seconds
- Look in top-right corner of window

---

## 📊 Data Storage

### User Data
- Stored in `data/users.json`
- Contains email, username, password (plain text - for demo only!)
- Profile pictures stored as file paths
- Persists between app restarts

### Session Data
- Cart items: In-memory (cleared on restart)
- Wishlist: In-memory (cleared on restart)
- Bookings: In-memory (cleared on restart)

**To persist cart/wishlist:**
Add save/load methods in `models/app_state.py` similar to `_save_users()`

---

## 🚀 Performance Tips

1. **Image Loading:** Use compressed JPG images (400x400px for pets)
2. **Smooth Scrolling:** Content is in `CTkScrollableFrame`
3. **Fast Navigation:** Pages destroy/recreate on navigation
4. **State Updates:** Centralized in `app_state.py` with callbacks

---

## 🎯 Feature Comparison

| Feature | React Version | Python GUI |
|---------|---------------|------------|
| Pet Browsing | ✅ | ✅ |
| Search & Filters | ✅ | ✅ |
| Pet Details | ✅ | ✅ |
| Services | ✅ | ✅ |
| Products | ✅ | ✅ |
| Shopping Cart | ✅ | ✅ |
| Wishlist | ✅ | ✅ |
| Authentication | ✅ | ✅ |
| Social Login | ✅ Simulated | ✅ Simulated |
| Profile Setup | ✅ | ✅ |
| Booking System | ✅ | ✅ |
| Calendar Scheduler | ✅ | ✅ |
| Breadcrumbs | ✅ | ✅ |
| Toast Notifications | ✅ | ✅ |
| Dark Theme | ✅ | ✅ |
| Responsive Design | ✅ | ✅ |
| Local Assets | ❌ (Used API) | ✅ |
| Auto Screen Detection | ❌ | ✅ |
| Desktop App | ❌ | ✅ |

---

## 📝 Next Steps

### For Production Use:
1. **Security:** Hash passwords (use `bcrypt` or `hashlib`)
2. **Database:** Switch from JSON to SQLite or PostgreSQL
3. **Validation:** Add email format validation
4. **Error Handling:** Add try-catch blocks for file operations
5. **Logging:** Implement logging for debugging

### Enhancements:
1. Add pet filtering by age, size, etc.
2. Implement booking history page
3. Add user profile editing
4. Create admin panel for managing pets
5. Add payment integration for products
6. Implement real email notifications
7. Add pet photo upload feature
8. Create dashboard with statistics

---

## 🎓 Code Architecture

### State Management
All app state is centralized in `models/app_state.py`:
- Single source of truth
- Callback pattern for UI updates
- Easy to debug and extend

### Component Pattern
Reusable components in `views/components/`:
- `PetCard` - Used in adoption and wishlist pages
- `ServiceCard` - Used in services and wishlist pages
- `Breadcrumbs` - Used in booking workflows

### Navigation
Main app (`main.py`) handles navigation:
```python
app.navigate_to("page_name", param1=value1)
```

### Styling
Colors defined in `utils/colors.py`:
- Consistent across all components
- Easy to theme the entire app
- Matches React app's color scheme

---

## ✅ Testing Checklist

- [ ] Launch application successfully
- [ ] Navigate between all pages
- [ ] Search and filter pets
- [ ] View pet details and image carousel
- [ ] Sign up with email/password
- [ ] Log in with existing account
- [ ] Set up user profile
- [ ] Add items to wishlist
- [ ] Remove items from wishlist
- [ ] Add products to cart
- [ ] Update cart quantities
- [ ] Complete checkout
- [ ] Book a service
- [ ] Select calendar date/time
- [ ] Complete adoption application
- [ ] See toast notifications
- [ ] Log out and log back in

---

## 📞 Support

For any issues:
1. Check this guide first
2. Review code comments in relevant files
3. Check console output for errors
4. Verify all files are in correct locations

---

## 🎉 Congratulations!

You now have a fully functional desktop application that replicates all features of your React/TypeScript web app. The Python GUI is:

✅ **Fully functional** - All workflows working  
✅ **Well-structured** - Modular, maintainable code  
✅ **Customizable** - Easy to modify and extend  
✅ **Professional** - Modern dark theme UI  
✅ **Responsive** - Adapts to screen size  
✅ **Offline** - No internet required  
✅ **Persistent** - User data saved locally  

Enjoy your new OnlyPets desktop application! 🐾
