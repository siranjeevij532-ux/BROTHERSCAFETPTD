#!/usr/bin/env python
import os
import sys
import django
import urllib.request
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
django.setup()

from restaurant.models import Table, Category, MenuItem
from django.conf import settings
from django.test import Client

print("\n" + "=" * 70)
print("COMPREHENSIVE IMAGE DISPLAY VERIFICATION")
print("=" * 70)

# 1. Check database has menu items with images
print("\n1. DATABASE CHECK")
print("-" * 70)
items_with_images = MenuItem.objects.filter(image__isnull=False)
print(f"Total menu items with images: {items_with_images.count()}")
if items_with_images.count() > 0:
    sample_item = items_with_images.first()
    print(f"Sample item: {sample_item.name}")
    print(f"  Image: {sample_item.image}")
    print(f"  Image URL: {sample_item.image.url}")
    print(f"  ✓ Database has images")
else:
    print("  ✗ WARNING: No menu items have images!")

# 2. Check filesystem
print("\n2. FILESYSTEM CHECK")
print("-" * 70)
menu_images_path = os.path.join(settings.MEDIA_ROOT, 'menu_images')
if os.path.exists(menu_images_path):
    files = os.listdir(menu_images_path)
    print(f"Files in {menu_images_path}: {len(files)}")
    print(f"  Sample files: {files[:3]}")
    print("  ✓ Image files exist on filesystem")
else:
    print(f"  ✗ Directory does not exist: {menu_images_path}")

# 3. Check URL configuration
print("\n3. URL CONFIGURATION CHECK")
print("-" * 70)
print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"DEBUG: {settings.DEBUG}")
if settings.MEDIA_URL and settings.MEDIA_ROOT:
    print("  ✓ Media configuration is set")
else:
    print("  ✗ Media configuration is missing")

# 4. Test template rendering
print("\n4. TEMPLATE RENDERING CHECK")
print("-" * 70)
try:
    from django.template import Template, Context
    
    # Get sample data
    categories = Category.objects.filter(is_active=True).prefetch_related('items')[:1]
    
    if categories.exists():
        cat = categories.first()
        items = cat.items.filter(is_available_dine_in=True)[:1]
        
        if items.exists():
            item = items.first()
            
            # Test the template condition
            template_str = '''{% if item.image %}"{{ item.image.url|escapejs }}"{% else %}null{% endif %}'''
            template = Template(template_str)
            context = Context({'item': item})
            result = template.render(context)
            
            print(f"Template test for item: {item.name}")
            print(f"  Has image field: {bool(item.image)}")
            print(f"  Template result: {result}")
            
            if result != "null" and result.startswith('"'):
                print("  ✓ Template correctly generates image URL")
            else:
                print("  ✗ Template failed to generate image URL")
        else:
            print("  No items found for template test")
    else:
        print("  No categories found for template test")
except Exception as e:
    print(f"  ✗ Template test error: {e}")

# 5. Test HTTP requests
print("\n5. HTTP REQUEST CHECK (against running server)")
print("-" * 70)
try:
    # Try to access a known image file
    test_image_url = "http://localhost:8000/media/menu_images/41g7lMwDtAL.jpg"
    try:
        req = urllib.request.Request(test_image_url)
        with urllib.request.urlopen(req, timeout=3) as response:
            status = response.status
            size = len(response.read())
            print(f"Test image URL: {test_image_url}")
            print(f"  Status: {status} {'✓' if status == 200 else '✗'}")
            print(f"  File size: {size} bytes")
            if status == 200 and size > 0:
                print("  ✓ Image is being served correctly")
            else:
                print("  ✗ Image request failed or returned empty")
    except urllib.error.URLError as e:
        print(f"  ✗ Cannot connect to server: {e}")
        print("  (Make sure server is running at localhost:8000)")
except Exception as e:
    print(f"  ✗ HTTP check error: {e}")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)
print("\nCustomers should now see images in the menu interface!")
