"""
Settings del proyecto Salud Vital.

Incluye:
- PostgreSQL configurado vía variables de entorno (.env)
- DRF y drf-spectacular (OpenAPI/Swagger)
- Separación de API y Web (templates en las apps)
"""

from pathlib import Path
import os
from dotenv import load_dotenv  # para leer variables desde .env

# BASE_DIR apunta a la carpeta raíz del proyecto (donde está manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables desde el archivo .env (ubicado junto a manage.py)
load_dotenv(BASE_DIR / ".env")

# =========================
# Seguridad / Debug
# =========================
# Clave secreta: en producción DEBE venir desde .env
SECRET_KEY = os.getenv("SECRET_KEY", "dev-inseguro-cambiar-en-produccion")

# DEBUG: en desarrollo True; en producción False
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Dominios/hosts permitidos (separados por comas en .env)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# =========================
# Apps instaladas
# =========================
INSTALLED_APPS = [
    # Núcleo de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'corsheaders',     # Permitir CORS en desarrollo (útil si hay front aparte)
    'rest_framework',  # Django REST Framework (API)
    'drf_spectacular', # Documentación OpenAPI/Swagger

    # Apps locales
    'clinica',
]

# =========================
# Middleware
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # debe ir arriba para inyectar headers CORS
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',  # incluye manejo de APPEND_SLASH, etc.
    'django.middleware.csrf.CsrfViewMiddleware', # protección CSRF para vistas web (no API)
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Módulo de URLS a nivel de proyecto
ROOT_URLCONF = 'salud_vital.urls'

# =========================
# Templates
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Si tuvieras una carpeta "templates" global al proyecto, agrégala aquí.
        # Usamos APP_DIRS=True para que busque templates dentro de cada app.
        'DIRS': [
            # BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Contexto útil en templates (request, user, messages, etc.)
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # necesario para usar "request" en templates/URL reversing
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Entradas para ASGI/WSGI
WSGI_APPLICATION = 'salud_vital.wsgi.application'
ASGI_APPLICATION = 'salud_vital.asgi.application'

# =========================
# Base de datos: PostgreSQL
# =========================
# Variables esperadas en .env:
#   DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',       # <- aquí se define Postgres
        'NAME': os.getenv('DB_NAME', 'Eva_2'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# =========================
# Validación de contraseñas
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# Internacionalización
# =========================
LANGUAGE_CODE = 'es'                 # Español
TIME_ZONE = 'America/Santiago'       # Huso horario de Chile
USE_I18N = True
USE_TZ = True

# =========================
# Archivos estáticos
# =========================
STATIC_URL = 'static/'
# En desarrollo puedes agregar rutas adicionales con STATICFILES_DIRS si tienes assets globales:
# STATICFILES_DIRS = [ BASE_DIR / 'assets' ]
# En producción normalmente defines STATIC_ROOT para collectstatic:
# STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# Django REST Framework
# =========================
REST_FRAMEWORK = {
    # Permisos por defecto: abierto para evaluación (ajusta si te piden auth)
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    # Generación de esquema OpenAPI con drf-spectacular
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# =========================
# drf-spectacular (OpenAPI/Swagger)
# =========================
SPECTACULAR_SETTINGS = {
    'TITLE': 'Salud Vital API',
    'DESCRIPTION': 'API de gestión clínica (Pacientes, Médicos, Consultas, etc.)',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # el JSON se sirve en /api/schema/
}

# =========================
# CORS (solo en desarrollo)
# =========================
CORS_ALLOW_ALL_ORIGINS = True if DEBUG else False