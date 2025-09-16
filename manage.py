#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# Ensure the nested django_project package is importable
# Adjust path below to point to the inner folder that contains settings.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'django_project'))

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
