import os
import sys
from django.core.wsgi import get_wsgi_application


def patch_django_python314():
    """
    Fix for Python 3.14 incompatibility with Django 4.2's Context.__copy__.
    Applied here so it also covers Gunicorn / Render deploys on Python 3.14.
    """
    try:
        import django.template.context as ctx_module
        if sys.version_info >= (3, 14):
            def _fixed_copy(self):
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.__dict__.update(self.__dict__)
                duplicate.dicts = self.dicts[:]
                return duplicate
            ctx_module.BaseContext.__copy__ = _fixed_copy
    except Exception:
        pass


patch_django_python314()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
application = get_wsgi_application()
