import sys
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve

admin.site.site_header = "Brothers Cafe - Admin Panel"
admin.site.site_title = "Brothers Cafe Admin"
admin.site.index_title = "Welcome to Brothers Cafe Management"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant.urls')),
]

# Always serve media files — needed in production (Render.com) for admin images
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
]

# Static files in dev
if settings.DEBUG or 'runserver' in sys.argv:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
