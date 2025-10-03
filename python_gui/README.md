# OnlyPets - Python GUI Application

A fully functional desktop application for pet adoption and services, converted from the React/TypeScript web application.

## Features

✨ **Complete Feature Set**
- 🐾 Pet adoption browsing with search and filters
- 💇 Service booking with calendar scheduler
- 🛍️ Product catalog with shopping cart
- ❤️ Wishlist functionality for pets and services
- 👤 User authentication (Sign in/Sign up with social login simulation)
- 📋 Multi-step booking workflows with breadcrumbs
- 🔔 Toast notifications for user feedback
- 📱 Responsive design that adapts to screen size

## Requirements

- Python 3.8 or higher
- Windows OS (tested on Windows 10/11)

## Installation

1. **Install Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up assets directory:**
   The application uses local images stored in the `assets/` directory. Run the asset generator to create placeholder images:
   ```bash
   python create_placeholder_assets.py
   ```
   
   Or manually add images to:
   - `assets/pets/` - Pet images (named `pet_01_1.jpg`, `pet_01_2.jpg`, etc.)
   - `assets/services/` - Service images
   - `assets/products/` - Product images
   - `assets/default_profile.png` - Default user profile icon

## Running the Application

```bash
python main.py
```

The application will automatically:
- Detect your screen size
- Launch maximized and centered
- Create necessary data directories

## Project Structure

```
python_gui/
├── main.py                 # Application entry point
├── models/
│   ├── types.py           # Data models
│   └── app_state.py       # Central state management
├── views/
│   ├── header.py          # Navigation header
│   ├── home_page.py       # Home page
│   ├── adoption_page.py   # Pet adoption listing
│   ├── pet_details_page.py # Individual pet details
│   ├── services_page.py   # Services listing
│   ├── products_page.py   # Products catalog
│   ├── cart_page.py       # Shopping cart
│   ├── wishlist_page.py   # User wishlist
│   ├── contact_page.py    # Contact form
│   ├── booking_page.py    # Multi-step booking workflow
│   ├── auth_modal.py      # Login/signup modal
│   ├── profile_modal.py   # Profile setup modal
│   ├── toast_container.py # Notification system
│   └── components/
│       ├── pet_card.py        # Pet card component
│       ├── service_card.py    # Service card component
│       └── breadcrumbs.py     # Progress indicator
├── utils/
│   └── colors.py          # Color scheme constants
├── assets/                # Images and icons
│   ├── pets/
│   ├── services/
│   ├── products/
│   └── default_profile.png
└── data/                  # User data storage
    └── users.json

```

## Features Guide

### Authentication
- Click "Sign In / Sign Up" in the header
- Create an account with email/password or use social login (simulated)
- Profile setup with username and profile picture
- User data persists between sessions

### Pet Adoption
1. Browse pets on the Adoption page
2. Use search bar or filters to find specific pets
3. Click on a pet card to view details
4. Click "ADOPT" to start the adoption process
5. Complete the multi-step form with personal info and adoption survey

### Service Booking
1. Navigate to Services page
2. Click "Book Now" on any service
3. Complete personal information
4. Select date and time slot on the calendar
5. Provide pet details
6. Review and confirm booking

### Shopping
1. Browse products on Products page
2. Add items to cart
3. View cart and adjust quantities
4. Proceed to checkout

### Wishlist
- Click the heart icon on pet or service cards
- View all favorites in the Wishlist page

## Customization

### Colors
Edit `utils/colors.py` to change the color scheme:
- Background colors (dark theme)
- Yellow accent color
- Text colors
- Status colors (success, error, info)

### Data
Sample pet and service data is in `models/app_state.py`. You can:
- Modify pet descriptions and facts
- Add/remove pets
- Change service offerings and pricing

### Images
Replace placeholder images in the `assets/` directory:
- Pet images: `pet_[id]_[1-4].jpg` (4 images per pet)
- Service images: Named after service type
- Product images: Named after product

## Tech Stack

- **GUI Framework:** CustomTkinter (modern, dark-themed tkinter)
- **Image Processing:** Pillow (PIL)
- **State Management:** Custom centralized state manager
- **Data Persistence:** JSON file storage

## Notes

- User data is stored locally in `data/users.json`
- Bookings and cart data reset on app restart (can be extended for persistence)
- Default profile icon is created automatically
- Application scales to fit screen resolution

## Troubleshooting

**Images not loading:**
- Ensure images exist in the correct `assets/` subdirectories
- Check file names match the expected pattern
- Run `create_placeholder_assets.py` to generate test images

**Application doesn't start:**
- Verify Python version (3.8+)
- Install all requirements: `pip install -r requirements.txt`
- Check for error messages in console

**Screen too small/large:**
- Application auto-detects screen size
- Content is scrollable and responsive
- Max width constraints prevent stretching on ultra-wide screens

## Future Enhancements

- Database integration (SQLite/PostgreSQL)
- Email notifications
- Payment processing integration
- Admin panel for managing pets and services
- Pet photo upload for user profiles
- Advanced search with multiple filters
- Booking history and management
- Real-time availability checking

## License

This project is a conversion of the OnlyPets React/TypeScript application to Python GUI.

## Support

For issues or questions, please refer to the code comments or create an issue.
