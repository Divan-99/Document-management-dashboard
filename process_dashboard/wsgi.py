"""
WSGI config for process_dashboard project.

Exposes the WSGI callable as a module-level variable named ``application``.
Use this with Gunicorn or waitress in production:
    waitress-serve --port=8000 process_dashboard.wsgi:application
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "process_dashboard.settings")

application = get_wsgi_application()
