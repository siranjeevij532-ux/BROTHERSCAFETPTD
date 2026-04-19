import os
import django
from django.template import Context, Template

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
django.setup()

from restaurant.models import MenuItem, Category

# Test that image URLs are properly formatted in template
print("\n" + "=" * 70)
print("TESTING IMAGE URL GENERATION IN TEMPLATE")
print("=" * 70)

categories = Category.objects.filter(is_active=True).prefetch_related('items')

print(f"\nTotal categories: {categories.count()}")
print(f"Categories with items: {categories.filter(items__isnull=False).distinct().count()}")

for cat in categories[:2]:
    items = cat.items.filter(is_available_dine_in=True)
    print(f"\n{'=' * 70}")
    print(f"Category: {cat.name}")
    print(f"Items count: {items.count()}")
    
    for item in items[:3]:
        has_image = item.image and bool(item.image.name)
        print(f"\n  Item: {item.name}")
        print(f"    Has image: {has_image}")
        if item.image:
            print(f"    Image field value: {item.image}")
            print(f"    Image name: {item.image.name}")
            print(f"    Image URL: {item.image.url}")
            print(f"    Image URL escaped: {item.image.url.replace('"', '&#34;')}")

print("\n" + "=" * 70)
print("IMAGE URL GENERATION TEST COMPLETE")
print("=" * 70)
