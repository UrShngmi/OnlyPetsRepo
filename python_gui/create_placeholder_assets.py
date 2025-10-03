"""
Asset generator - Creates placeholder images for the application
Run this script to generate placeholder images if you don't have real pet/service images
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(path, width, height, text, bg_color, text_color):
    """Create a placeholder image with text"""
    # Create image
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", 40)
        small_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2 - 20
    
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Add "placeholder" label
    placeholder_text = "Placeholder Image"
    bbox2 = draw.textbbox((0, 0), placeholder_text, font=small_font)
    text_width2 = bbox2[2] - bbox2[0]
    x2 = (width - text_width2) // 2
    y2 = y + text_height + 30
    
    draw.text((x2, y2), placeholder_text, fill=text_color, font=small_font)
    
    # Save
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'JPEG', quality=85)
    print(f"Created: {path}")

def create_default_profile():
    """Create default profile icon"""
    size = 200
    img = Image.new('RGB', (size, size), color='#374151')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple user icon
    # Head circle
    head_radius = 40
    head_center = (size // 2, size // 2 - 20)
    draw.ellipse([
        head_center[0] - head_radius,
        head_center[1] - head_radius,
        head_center[0] + head_radius,
        head_center[1] + head_radius
    ], fill='#9ca3af')
    
    # Body semi-circle
    body_width = 80
    body_height = 50
    body_center = (size // 2, size // 2 + 50)
    draw.ellipse([
        body_center[0] - body_width,
        body_center[1] - body_height,
        body_center[0] + body_width,
        body_center[1] + body_height
    ], fill='#9ca3af')
    
    path = 'assets/default_profile.png'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.save(path, 'PNG')
    print(f"Created: {path}")

def main():
    """Generate all placeholder images"""
    print("Generating placeholder assets...")
    
    # Pet images (12 pets, 4 images each)
    pet_colors = [
        ('#d97706', 'white'),  # Orange
        ('#3b82f6', 'white'),  # Blue
        ('#10b981', 'white'),  # Green
        ('#8b5cf6', 'white'),  # Purple
        ('#f59e0b', 'black'),  # Yellow
        ('#ef4444', 'white'),  # Red
        ('#06b6d4', 'white'),  # Cyan
        ('#ec4899', 'white'),  # Pink
        ('#84cc16', 'white'),  # Lime
        ('#6366f1', 'white'),  # Indigo
        ('#14b8a6', 'white'),  # Teal
        ('#f97316', 'white'),  # Orange-red
    ]
    
    pet_names = [
        "Buddy", "Whiskers", "Charlie", "Luna", "Max", "Tweety",
        "Bella", "Rocky", "Mittens", "Daisy", "Coco", "Shadow"
    ]
    
    for i in range(12):
        pet_id = f"pet_{i+1:02d}"
        pet_name = pet_names[i]
        bg_color, text_color = pet_colors[i]
        
        for img_num in range(1, 5):
            path = f'assets/pets/{pet_id}_{img_num}.jpg'
            create_placeholder_image(
                path, 400, 400,
                f"{pet_name}\n#{img_num}",
                bg_color, text_color
            )
    
    # Service images
    services = [
        ('grooming', 'Grooming', '#10b981', 'white'),
        ('health_checkup', 'Health\nCheckup', '#3b82f6', 'white'),
        ('training', 'Training', '#8b5cf6', 'white'),
        ('pet_sitting', 'Pet\nSitting', '#f59e0b', 'black'),
        ('dog_walking', 'Dog\nWalking', '#06b6d4', 'white'),
    ]
    
    for filename, text, bg_color, text_color in services:
        path = f'assets/services/{filename}.jpg'
        create_placeholder_image(
            path, 600, 400,
            text,
            bg_color, text_color
        )
    
    # Product images
    products = [
        ('pet_food', 'Pet Food', '#84cc16', 'white'),
        ('pet_toy', 'Pet Toy', '#ec4899', 'white'),
        ('pet_bed', 'Pet Bed', '#6366f1', 'white'),
        ('pet_leash', 'Leash &\nCollar', '#f97316', 'white'),
    ]
    
    for filename, text, bg_color, text_color in products:
        path = f'assets/products/{filename}.jpg'
        create_placeholder_image(
            path, 400, 400,
            text,
            bg_color, text_color
        )
    
    # Default profile icon
    create_default_profile()
    
    print("\n✅ All placeholder assets created successfully!")
    print("\nAssets generated:")
    print("- 48 pet images (12 pets × 4 images each)")
    print("- 5 service images")
    print("- 4 product images")
    print("- 1 default profile icon")
    print("\nYou can now run the application: python main.py")

if __name__ == "__main__":
    main()
