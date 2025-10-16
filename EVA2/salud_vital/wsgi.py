"""
Configuración WSGI del proyecto (para servidores como gunicorn/uwsgi).
La mayoría de despliegues tradicionales usan WSGI.
"""
import os
from django.core.wsgi import get_wsgi_application

# Apunta al módulo de settings de este proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')

# Objeto WSGI que el servidor va a usar
application = get_wsgi_application()