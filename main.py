import os
import sys
from metamystic.wsgi import application

app = application

if __name__ == "__main__":
    # Add support for gunicorn running
    port = int(os.environ.get("PORT", 5000))
    
    if len(sys.argv) > 1:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        # Run with Gunicorn-compatible settings
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])
