# EVA2/clinica/urls_web.py
# ---------------------------------------------------------
# Rutas para la interfaz WEB (templates HTML).
# La API queda en clinica/urls.py (DRF).
# ---------------------------------------------------------

from django.urls import path
from .views_web import (
    HomeView,
    PacienteList, PacienteCreate, PacienteUpdate, PacienteDelete,
    MedicoList, MedicoCreate, MedicoUpdate, MedicoDelete,
    EspecialidadList, EspecialidadCreate, EspecialidadUpdate, EspecialidadDelete,
    ConsultaList, ConsultaCreate, ConsultaUpdate, ConsultaDelete,
    TratamientoList, TratamientoCreate, TratamientoUpdate, TratamientoDelete,
    MedicamentoList, MedicamentoCreate, MedicamentoUpdate, MedicamentoDelete,
    RecetaList, RecetaCreate, RecetaUpdate, RecetaDelete,
    SeguroList, SeguroCreate, SeguroUpdate, SeguroDelete,
    PacienteSeguroList, PacienteSeguroCreate, PacienteSeguroUpdate, PacienteSeguroDelete,
)

urlpatterns = [
    # Home (dashboard de navegación)
    path("", HomeView.as_view(), name="clinica_home"),

    # Pacientes
    path("pacientes/", PacienteList.as_view(), name="paciente_list"),
    path("pacientes/nuevo/", PacienteCreate.as_view(), name="paciente_create"),
    path("pacientes/<int:pk>/editar/", PacienteUpdate.as_view(), name="paciente_update"),
    path("pacientes/<int:pk>/eliminar/", PacienteDelete.as_view(), name="paciente_delete"),

    # Médicos
    path("medicos/", MedicoList.as_view(), name="medico_list"),
    path("medicos/nuevo/", MedicoCreate.as_view(), name="medico_create"),
    path("medicos/<int:pk>/editar/", MedicoUpdate.as_view(), name="medico_update"),
    path("medicos/<int:pk>/eliminar/", MedicoDelete.as_view(), name="medico_delete"),

    # Especialidades
    path("especialidades/", EspecialidadList.as_view(), name="especialidad_list"),
    path("especialidades/nuevo/", EspecialidadCreate.as_view(), name="especialidad_create"),
    path("especialidades/<int:pk>/editar/", EspecialidadUpdate.as_view(), name="especialidad_update"),
    path("especialidades/<int:pk>/eliminar/", EspecialidadDelete.as_view(), name="especialidad_delete"),

    # Consultas
    path("consultas/", ConsultaList.as_view(), name="consulta_list"),
    path("consultas/nuevo/", ConsultaCreate.as_view(), name="consulta_create"),
    path("consultas/<int:pk>/editar/", ConsultaUpdate.as_view(), name="consulta_update"),
    path("consultas/<int:pk>/eliminar/", ConsultaDelete.as_view(), name="consulta_delete"),

    # Tratamientos
    path("tratamientos/", TratamientoList.as_view(), name="tratamiento_list"),
    path("tratamientos/nuevo/", TratamientoCreate.as_view(), name="tratamiento_create"),
    path("tratamientos/<int:pk>/editar/", TratamientoUpdate.as_view(), name="tratamiento_update"),
    path("tratamientos/<int:pk>/eliminar/", TratamientoDelete.as_view(), name="tratamiento_delete"),

    # Medicamentos
    path("medicamentos/", MedicamentoList.as_view(), name="medicamento_list"),
    path("medicamentos/nuevo/", MedicamentoCreate.as_view(), name="medicamento_create"),
    path("medicamentos/<int:pk>/editar/", MedicamentoUpdate.as_view(), name="medicamento_update"),
    path("medicamentos/<int:pk>/eliminar/", MedicamentoDelete.as_view(), name="medicamento_delete"),

    # Recetas
    path("recetas/", RecetaList.as_view(), name="receta_list"),
    path("recetas/nuevo/", RecetaCreate.as_view(), name="receta_create"),
    path("recetas/<int:pk>/editar/", RecetaUpdate.as_view(), name="receta_update"),
    path("recetas/<int:pk>/eliminar/", RecetaDelete.as_view(), name="receta_delete"),

    # Seguros
    path("seguros/", SeguroList.as_view(), name="seguro_list"),
    path("seguros/nuevo/", SeguroCreate.as_view(), name="seguro_create"),
    path("seguros/<int:pk>/editar/", SeguroUpdate.as_view(), name="seguro_update"),
    path("seguros/<int:pk>/eliminar/", SeguroDelete.as_view(), name="seguro_delete"),

    # Afiliaciones Paciente–Seguro
    path("afiliaciones/", PacienteSeguroList.as_view(), name="paciente_seguro_list"),
    path("afiliaciones/nuevo/", PacienteSeguroCreate.as_view(), name="paciente_seguro_create"),
    path("afiliaciones/<int:pk>/editar/", PacienteSeguroUpdate.as_view(), name="paciente_seguro_update"),
    path("afiliaciones/<int:pk>/eliminar/", PacienteSeguroDelete.as_view(), name="paciente_seguro_delete"),
]