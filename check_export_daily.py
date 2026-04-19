import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(is_staff=True).first()
print('staff', u)
if u:
    c = Client()
    c.force_login(u)
    r = c.get('/staff/export/daily/')
    print('status', r.status_code)
    print('content_type', r.get('Content-Type'))
    print('disposition', r.get('Content-Disposition'))
    print('length', len(r.content))
    print(r.content[:200])
else:
    print('no staff user found')
