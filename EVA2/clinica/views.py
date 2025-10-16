# EVA2/clinica/views.py
# ---------------------------------------------------------
# Vistas de la API (DRF) — ViewSets.
# El ruteo de estos ViewSets está en clinica/urls.py
# ---------------------------------------------------------

from rest_framework import viewsets, permissions
from .models import (
    Paciente, Medico, Especialidad,
    ConsultaMedica, Tratamiento, Medicamento,
    RecetaMedica, SeguroSalud, PacienteSeguro
)
from .serializers import (
    PacienteSerializer, MedicoSerializer, EspecialidadSerializer,
    ConsultaMedicaSerializer, TratamientoSerializer, MedicamentoSerializer,
    RecetaMedicaSerializer, SeguroSaludSerializer, PacienteSeguroSerializer
)

class BaseModelViewSet(viewsets.ModelViewSet):
    """
    Comportamiento común:
      - Permitir lectura a cualquiera y escritura abierta para evaluación.
        (ajusta permisos según lo que te pidan)
    """
    permission_classes = [permissions.AllowAny]


class PacienteViewSet(BaseModelViewSet):
    queryset = Paciente.objects.all().order_by("id")
    serializer_class = PacienteSerializer


class MedicoViewSet(BaseModelViewSet):
    queryset = Medico.objects.all().order_by("id")
    serializer_class = MedicoSerializer


class EspecialidadViewSet(BaseModelViewSet):
    queryset = Especialidad.objects.all().order_by("id")
    serializer_class = EspecialidadSerializer


class ConsultaMedicaViewSet(BaseModelViewSet):
    queryset = ConsultaMedica.objects.select_related("paciente", "medico").all().order_by("-fecha_consulta")
    serializer_class = ConsultaMedicaSerializer


class TratamientoViewSet(BaseModelViewSet):
    queryset = Tratamiento.objects.select_related("consulta").all().order_by("-id")
    serializer_class = TratamientoSerializer


class MedicamentoViewSet(BaseModelViewSet):
    queryset = Medicamento.objects.all().order_by("nombre")
    serializer_class = MedicamentoSerializer


class RecetaMedicaViewSet(BaseModelViewSet):
    queryset = RecetaMedica.objects.select_related("tratamiento", "medicamento").all().order_by("-id")
    serializer_class = RecetaMedicaSerializer


class SeguroSaludViewSet(BaseModelViewSet):
    queryset = SeguroSalud.objects.all().order_by("nombre")
    serializer_class = SeguroSaludSerializer


class PacienteSeguroViewSet(BaseModelViewSet):
    queryset = PacienteSeguro.objects.select_related("paciente", "seguro").all().order_by("-id")
    serializer_class = PacienteSeguroSerializer