from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa ÚNICAMENTE los ViewSets de la API (no las vistas HTML)
from .views import (
    PacienteViewSet,
    MedicoViewSet,
    EspecialidadViewSet,
    ConsultaMedicaViewSet,
    TratamientoViewSet,
    MedicamentoViewSet,
    RecetaMedicaViewSet,
    SeguroSaludViewSet,
    PacienteSeguroViewSet,
)

# Router de DRF:
# - DefaultRouter crea automáticamente las rutas CRUD por recurso:
#   GET    /<recurso>/          -> list
#   POST   /<recurso>/          -> create
#   GET    /<recurso>/<id>/     -> retrieve
#   PUT    /<recurso>/<id>/     -> update
#   PATCH  /<recurso>/<id>/     -> partial_update
#   DELETE /<recurso>/<id>/     -> destroy
# - Usa slash final por defecto (ej: /api/pacientes/).
router = DefaultRouter()

# Registra cada ViewSet con un prefijo. Ejemplos resultantes:
#   /api/pacientes/ , /api/pacientes/1/
router.register(r"pacientes", PacienteViewSet, basename="paciente")

#   /api/medicos/ , /api/medicos/1/
router.register(r"medicos", MedicoViewSet, basename="medico")

#   /api/especialidades/ , /api/especialidades/1/
router.register(r"especialidades", EspecialidadViewSet, basename="especialidad")

#   /api/consultas/ , /api/consultas/1/
router.register(r"consultas", ConsultaMedicaViewSet, basename="consulta")

#   /api/tratamientos/ , /api/tratamientos/1/
router.register(r"tratamientos", TratamientoViewSet, basename="tratamiento")

#   /api/medicamentos/ , /api/medicamentos/1/
router.register(r"medicamentos", MedicamentoViewSet, basename="medicamento")

#   /api/recetas/ , /api/recetas/1/
router.register(r"recetas", RecetaMedicaViewSet, basename="receta")

#   /api/seguros/ , /api/seguros/1/
router.register(r"seguros", SeguroSaludViewSet, basename="seguro")

#   /api/afiliaciones/ , /api/afiliaciones/1/
router.register(r"afiliaciones", PacienteSeguroViewSet, basename="paciente-seguro")

urlpatterns = [
    # Incluye todas las rutas generadas por el router:
    #   /api/pacientes/, /api/medicos/, etc.
    path("", include(router.urls)),

    # Autenticación para la API navegable de DRF (opcional):
    #   /api/auth/login/  y /api/auth/logout/
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]