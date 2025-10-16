#!/usr/bin/env python
# Este script es el punto de entrada para comandos Django (runserver, migrate, etc.)
import os
import sys

def main():
    # Indica a Django qué settings usar (el módulo del proyecto)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'salud_vital.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Error típico si el venv no está activado o no está instalado Django
        raise ImportError("No se pudo importar Django. ¿Está activado el entorno virtual?") from exc
    # Reenvía los argumentos a Django (ej: runserver, makemigrations)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()