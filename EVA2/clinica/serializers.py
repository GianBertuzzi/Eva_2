# clinica/serializers.py
from rest_framework import serializers
from .models import (
    Paciente, Medico, Especialidad, ConsultaMedica,
    Tratamiento, Medicamento, RecetaMedica,
    SeguroSalud, PacienteSeguro
)

# Un serializer por modelo: transforma entre objetos Django <-> JSON

class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"

class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = "__all__"

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = "__all__"

class ConsultaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultaMedica
        fields = "__all__"

class TratamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tratamiento
        fields = "__all__"

class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = "__all__"

class RecetaMedicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaMedica
        fields = "__all__"

class SeguroSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeguroSalud
        fields = "__all__"

class PacienteSeguroSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacienteSeguro
        fields = "__all__"
