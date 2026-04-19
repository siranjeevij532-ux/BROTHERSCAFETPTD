#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
django.setup()

from django.conf import settings

print(f"MEDIA_URL: {settings.MEDIA_URL}")
print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
print(f"MEDIA_ROOT exists: {os.path.exists(settings.MEDIA_ROOT)}")
print(f"DEBUG: {settings.DEBUG}")

# Check if actual image files exist
menu_images_dir = os.path.join(settings.MEDIA_ROOT, 'menu_images')
print(f"Menu images dir exists: {os.path.exists(menu_images_dir)}")
if os.path.exists(menu_images_dir):
    files = os.listdir(menu_images_dir)
    print(f"Files in menu_images: {files[:3]}")
