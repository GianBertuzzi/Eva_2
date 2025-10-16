"""
URLS del proyecto.

- /admin/           -> Django Admin
- /api/             -> Endpoints de la API (DRF) definidos en clinica/urls.py
- /api/schema/      -> OpenAPI JSON (drf-spectacular)
- /api/docs/        -> Swagger UI (drf-spectacular)
- /clinica/         -> Vistas HTML (templates) en clinica/urls_web.py
- 404 custom        -> Usa el template clinica/404.html cuando DEBUG=False
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.shortcuts import render

urlpatterns = [
    # Panel de administración
    path('admin/', admin.site.urls),

    # API (router de DRF definido en clinica/urls.py)
    path('api/', include('clinica.urls')),

    # Documentación OpenAPI (JSON) y Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema-json'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),

    # Vistas HTML (templates) de la app clínica (separadas de la API)
    path('clinica/', include('clinica.urls_web')),
]

# ============== 404 personalizado ==============
# Importante:
# - Este handler se usará cuando DEBUG = False (en DEBUG=True verás el 404 de Django)
def custom_404(request, exception):
    # Renderiza el template de 404 de la app clinica
    return render(request, "clinica/404.html", status=404)

# Registra el handler a nivel de proyecto
handler404 = "salud_vital.urls.custom_404"
