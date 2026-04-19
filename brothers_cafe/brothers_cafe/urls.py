from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.admin import AdminSite

admin.site.site_header = "Brothers Cafe - Admin Panel"
admin.site.site_title = "Brothers Cafe Admin"
admin.site.index_title = "Welcome to Brothers Cafe Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
