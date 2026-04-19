import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
django.setup()

from restaurant.models import MenuItem, Category
from django.conf import settings

print("=" * 60)
print("VERIFYING IMAGE CONFIGURATION")
print("=" * 60)

# Check settings
print(f"\nMEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")
print(f"DEBUG: {settings.DEBUG}")

# Check menu items with images
print("\n" + "=" * 60)
print("MENU ITEMS WITH IMAGES")
print("=" * 60)
items = MenuItem.objects.filter(image__isnull=False)[:5]
for item in items:
    if item.image:
        print(f"\n✓ {item.name}")
        print(f"  Image file: {item.image.name}")
        print(f"  Image URL: {item.image.url}")
        print(f"  Full URL: http://localhost:8000{item.image.url}")
        file_path = os.path.join(settings.MEDIA_ROOT, item.image.name)
        print(f"  File exists: {os.path.exists(file_path)}")

# Check categories with images
print("\n" + "=" * 60)
print("CATEGORIES WITH IMAGES")
print("=" * 60)
categories = Category.objects.filter(image__isnull=False)[:5]
for cat in categories:
    if cat.image:
        print(f"\n✓ {cat.name}")
        print(f"  Image file: {cat.image.name}")
        print(f"  Image URL: {cat.image.url}")
        print(f"  Full URL: http://localhost:8000{cat.image.url}")
        file_path = os.path.join(settings.MEDIA_ROOT, cat.image.name)
        print(f"  File exists: {os.path.exists(file_path)}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
