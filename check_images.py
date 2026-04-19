#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
sys.path.append('.')
django.setup()

from restaurant.models import MenuItem, Category

print("Menu Items with images:")
items = MenuItem.objects.filter(image__isnull=False)[:5]
for item in items:
    print(f"{item.name}: {item.image.url}")

print("\nCategories with images:")
categories = Category.objects.filter(image__isnull=False)[:5]
for cat in categories:
    print(f"{cat.name}: {cat.image.url}")