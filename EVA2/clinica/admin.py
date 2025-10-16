from django.contrib import admin
from .models import (Especialidad, Medico, Paciente, ConsultaMedica,
                     Tratamiento, Medicamento, RecetaMedica,
                     SeguroSalud, PacienteSeguro)

admin.site.register(Especialidad)
admin.site.register(Medico)
admin.site.register(Paciente)
admin.site.register(ConsultaMedica)
admin.site.register(Tratamiento)
admin.site.register(Medicamento)
admin.site.register(RecetaMedica)
admin.site.register(SeguroSalud)
admin.site.register(PacienteSeguro)