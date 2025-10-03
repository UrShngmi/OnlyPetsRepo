"""
Quick test script to verify fixes
"""
import os
import sys

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

# Test 1: Check if service assets exist
print("=" * 50)
print("TEST 1: Checking service assets...")
print("=" * 50)

service_assets = ['grooming.png', 'checkup.png', 'training.png', 'sitting.png', 'walking.png']
assets_dir = os.path.join(os.path.dirname(__file__), 'assets', 'services')

for asset in service_assets:
    asset_path = os.path.join(assets_dir, asset)
    exists = os.path.exists(asset_path)
    status = "[FOUND]" if exists else "[MISSING]"
    print(f"{status}: {asset}")

# Test 2: Check if product assets exist
print("\n" + "=" * 50)
print("TEST 2: Checking product assets...")
print("=" * 50)

product_assets = ['petfood.png']
assets_dir = os.path.join(os.path.dirname(__file__), 'assets', 'products')

for asset in product_assets:
    asset_path = os.path.join(assets_dir, asset)
    exists = os.path.exists(asset_path)
    status = "[FOUND]" if exists else "[MISSING]"
    print(f"{status}: {asset}")

# Test 3: Check booking_page.py for confirmation method
print("\n" + "=" * 50)
print("TEST 3: Checking booking_page.py confirmation method...")
print("=" * 50)

booking_file = os.path.join(os.path.dirname(__file__), 'views', 'booking_page.py')
with open(booking_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Check if _render_confirmation has no parent parameter
    if 'def _render_confirmation(self):' in content:
        print("[PASS] _render_confirmation method signature is correct")
    else:
        print("[FAIL] _render_confirmation method signature is incorrect")
    
    # Check if confirmation uses proper centering (either place or grid)
    if ('center_frame.place(relx=0.5, rely=0.5, anchor="center")' in content or 
        'center_frame.grid(row=0, column=0' in content):
        print("[PASS] Confirmation uses proper centering")
    else:
        print("[FAIL] Confirmation centering may be incorrect")
    
    # Check if Back to Homepage button exists
    if 'Back to Homepage' in content:
        print("[PASS] Back to Homepage button exists")
    else:
        print("[FAIL] Back to Homepage button missing")

# Test 4: Check service_card.py for background image loading
print("\n" + "=" * 50)
print("TEST 4: Checking service_card.py background loading...")
print("=" * 50)

service_card_file = os.path.join(os.path.dirname(__file__), 'views', 'components', 'service_card.py')
with open(service_card_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Check if ImageEnhance is imported
    if 'from PIL import Image, ImageTk, ImageEnhance' in content:
        print("[PASS] ImageEnhance imported")
    else:
        print("[FAIL] ImageEnhance not imported")
    
    # Check if brightness enhancement is used
    if 'ImageEnhance.Brightness' in content and ('enhance(0.4)' in content or 'enhance(0.3)' in content):
        print("[PASS] Image darkening implemented")
    else:
        print("[FAIL] Image darkening not implemented")

# Test 5: Check app_state.py for correct service image URLs
print("\n" + "=" * 50)
print("TEST 5: Checking app_state.py service image URLs...")
print("=" * 50)

app_state_file = os.path.join(os.path.dirname(__file__), 'models', 'app_state.py')
with open(app_state_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
    correct_urls = [
        'assets/services/grooming.png',
        'assets/services/checkup.png',
        'assets/services/training.png',
        'assets/services/sitting.png',
        'assets/services/walking.png'
    ]
    
    all_correct = all(url in content for url in correct_urls)
    
    if all_correct:
        print("[PASS] All service image URLs are correct")
    else:
        print("[FAIL] Some service image URLs are incorrect")
        for url in correct_urls:
            if url not in content:
                print(f"  Missing: {url}")

# Test 6: Check service card text colors
print("\n" + "=" * 50)
print("TEST 6: Checking service card text colors...")
print("=" * 50)

service_card_file = os.path.join(os.path.dirname(__file__), 'views', 'components', 'service_card.py')
with open(service_card_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Check if text colors are white for better visibility
    if 'text_color="white"' in content:
        print("[PASS] Service card uses white text for overlay")
    else:
        print("[FAIL] Service card text color may not be optimal")
    
    # Check if brightness is reduced enough
    if 'enhance(0.3)' in content:
        print("[PASS] Image darkening is optimal (30%)")
    else:
        print("[FAIL] Image darkening may not be optimal")

# Test 7: Check confirmation page centering
print("\n" + "=" * 50)
print("TEST 7: Checking confirmation page centering...")
print("=" * 50)

booking_file = os.path.join(os.path.dirname(__file__), 'views', 'booking_page.py')
with open(booking_file, 'r', encoding='utf-8') as f:
    content = f.read()
    
    # Check if grid centering is used
    if 'grid_rowconfigure(0, weight=1)' in content and 'grid_columnconfigure(0, weight=1)' in content:
        print("[PASS] Confirmation page uses proper grid centering")
    else:
        print("[FAIL] Confirmation page centering may be incorrect")

print("\n" + "=" * 50)
print("TEST SUMMARY")
print("=" * 50)
print("All tests completed. Review results above.")
print("If all tests show [PASS], the fixes should be working correctly.")
print("=" * 50)
