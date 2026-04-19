#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def patch_django_python314():
    """
    Fix for Python 3.14 incompatibility with Django 4.2's Context.__copy__.
    The copy(super()) call fails on Python 3.14 because super() objects no
    longer support __dict__ assignment. This monkey-patch fixes it.
    """
    try:
        import django.template.context as ctx_module
        import sys as _sys

        if _sys.version_info >= (3, 14):
            original_copy = ctx_module.BaseContext.__copy__

            def _fixed_copy(self):
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.__dict__.update(self.__dict__)
                duplicate.dicts = self.dicts[:]
                return duplicate

            ctx_module.BaseContext.__copy__ = _fixed_copy
    except Exception:
        pass  # If it fails, let Django raise its own error


patch_django_python314()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brothers_cafe.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
