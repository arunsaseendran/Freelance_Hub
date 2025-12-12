"""
Script to create placeholder images for services
"""
import os
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelancer_platform.settings')
django.setup()

from services.models import Service, Category
from django.core.files import File
from pathlib import Path

# Create media directory if it doesn't exist
MEDIA_ROOT = Path(__file__).resolve().parent / 'media' / 'services'
MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

# Service category colors and icons
CATEGORY_THEMES = {
    'Home Cleaning': {'color': (79, 172, 254), 'emoji': '🧹'},
    'Electrical Work': {'color': (255, 193, 7), 'emoji': '⚡'},
    'Beauty Care': {'color': (240, 147, 251), 'emoji': '💄'},
    'Plumbing': {'color': (0, 242, 254), 'emoji': '🔧'},
    'Tutoring': {'color': (102, 126, 234), 'emoji': '📚'},
    'Carpentry': {'color': (139, 69, 19), 'emoji': '🪚'},
    'Painting': {'color': (156, 39, 176), 'emoji': '🎨'},
    'Gardening': {'color': (76, 175, 80), 'emoji': '🌱'},
}

def create_service_image(service_title, category_name, filename):
    """Create a professional placeholder image for a service"""
    
    # Image dimensions
    width, height = 800, 600
    
    # Get category theme
    theme = CATEGORY_THEMES.get(category_name, {'color': (102, 126, 234), 'emoji': '🔧'})
    base_color = theme['color']
    
    # Create gradient background
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    
    # Create gradient from dark to light
    for y in range(height):
        # Calculate color for this row
        factor = y / height
        r = int(base_color[0] * (0.3 + 0.7 * factor))
        g = int(base_color[1] * (0.3 + 0.7 * factor))
        b = int(base_color[2] * (0.3 + 0.7 * factor))
        draw.rectangle([(0, y), (width, y + 1)], fill=(r, g, b))
    
    # Add overlay pattern
    for i in range(0, width, 100):
        for j in range(0, height, 100):
            draw.ellipse([(i, j), (i + 50, j + 50)], fill=(255, 255, 255, 10))
    
    # Try to add text (will work without custom fonts)
    try:
        # Use default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    except:
        font_large = None
        font_small = None
    
    # Add category name at top
    if font_small:
        category_text = category_name.upper()
        bbox = draw.textbbox((0, 0), category_text, font=font_small)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) // 2, 50), category_text, 
                 fill=(255, 255, 255, 200), font=font_small)
    
    # Add service title in center
    if font_large:
        # Wrap text if too long
        words = service_title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=font_large)
            if bbox[2] - bbox[0] > width - 100:
                current_line.pop()
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Draw lines
        y_offset = (height - len(lines) * 40) // 2
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font_large)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) // 2, y_offset), line, 
                     fill=(255, 255, 255), font=font_large)
            y_offset += 40
    
    # Add decorative elements
    draw.ellipse([(width - 150, -50), (width + 50, 150)], 
                fill=(255, 255, 255, 20))
    draw.ellipse([(-50, height - 150), (150, height + 50)], 
                fill=(255, 255, 255, 20))
    
    # Save image
    filepath = MEDIA_ROOT / filename
    image.save(filepath, 'JPEG', quality=85)
    
    return filepath

def add_images_to_services():
    """Add placeholder images to all services without images"""
    
    print("Adding images to services...")
    
    services = Service.objects.filter(image='')
    updated_count = 0
    
    for service in services:
        try:
            # Create filename
            filename = f"service_{service.id}_{service.title[:30].replace(' ', '_').lower()}.jpg"
            
            # Create image
            filepath = create_service_image(
                service.title,
                service.category.name,
                filename
            )
            
            # Attach to service
            with open(filepath, 'rb') as f:
                service.image.save(filename, File(f), save=True)
            
            print(f"SUCCESS: Added image to '{service.title}'")
            updated_count += 1
            
        except Exception as e:
            print(f"ERROR: Failed to add image to '{service.title}': {str(e)}")
    
    print(f"\nSUCCESS: Added images to {updated_count} services!")

if __name__ == '__main__':
    add_images_to_services()
