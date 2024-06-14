import imp

import os
import sys
from django.core.wsgi import get_wsgi_application

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))


# Set the environment variable to tell Django where your settings module is located
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Get the WSGI application
application = get_wsgi_application()