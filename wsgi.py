"""
WSGI config for metamystic project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
import sys

# Add the project directory to the sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variable for Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metamystic.settings")

# Set up the Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()