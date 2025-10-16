"""
Configuración ASGI del proyecto (para servidores async como Uvicorn/Hypercorn).
Solo necesitas esto si sirves la app con ASGI o usas websockets (Channels).
"""
import os
from django.core.asgi import get_asgi_application

# Apunta al módulo de settings de este proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')

# Objeto ASGI que el servidor va a usar
application = get_asgi_application()
