# EVA2/clinica/views_web.py
# ---------------------------------------------------------
# Vistas de la interfaz WEB (templates HTML).
# - HomeView entrega "menu_items" al template de inicio.
# - List/Create/Update/Delete para cada modelo.
# - SafeDeleteMixin: evita borrar si hay relaciones (muestra motivo).
# ---------------------------------------------------------

from django.contrib import messages
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView

from .models import (
    Paciente, Medico, Especialidad,
    ConsultaMedica, Tratamiento, Medicamento,
    RecetaMedica, SeguroSalud, PacienteSeguro
)

# ---------- Home ----------
class HomeView(TemplateView):
    """Home simple con tarjetas de navegación."""
    template_name = "clinica/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["menu_items"] = [
            ("Pacientes",      "people",           "paciente_list"),
            ("Médicos",        "person-heart",     "medico_list"),
            ("Especialidades", "diagram-3",        "especialidad_list"),
            ("Consultas",      "clipboard2-pulse", "consulta_list"),
            ("Tratamientos",   "activity",         "tratamiento_list"),
            ("Medicamentos",   "capsule-pill",     "medicamento_list"),
            ("Recetas",        "file-medical",     "receta_list"),
            ("Seguros",        "shield-check",     "seguro_list"),
            ("Afiliaciones",   "link-45deg",       "paciente_seguro_list"),
        ]
        return ctx


# ---------- Mixins de utilidad ----------
class PageNamesMixin:
    """Inyecta en el contexto los nombres de URL que usan las tablas (editar/eliminar)."""
    page_update_name: str = ""
    page_delete_name: str = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_update"] = self.page_update_name
        ctx["page_delete"] = self.page_delete_name
        return ctx


class FormExtrasMixin:
    """Agrega page_title y cancel_url a los formularios."""
    page_title: str = ""
    cancel_url_name: str = ""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["page_title"] = self.page_title or "Formulario"
        if self.cancel_url_name:
            ctx["cancel_url"] = reverse(self.cancel_url_name)
        return ctx


class SafeDeleteMixin:
    """
    Evita eliminar objetos que tienen relaciones protegidas.
    - GET: pasa 'cannot_delete_reason' al template si hay dependencias.
    - POST: captura ProtectedError, muestra mensaje y redirige a la lista.
    """
    success_url = None
    cancel_url_name: str = ""
    model = None

    def related_reasons(self, obj):
        reasons = []
        if isinstance(obj, Paciente):
            if ConsultaMedica.objects.filter(paciente=obj).exists():
                reasons.append("Tiene consultas médicas registradas.")
            if PacienteSeguro.objects.filter(paciente=obj).exists():
                reasons.append("Tiene afiliaciones de seguro de salud.")
        if isinstance(obj, Medico):
            if ConsultaMedica.objects.filter(medico=obj).exists():
                reasons.append("Tiene consultas médicas asignadas.")
        if isinstance(obj, Especialidad):
            if Medico.objects.filter(especialidad=obj).exists():
                reasons.append("Existen médicos con esta especialidad.")
        if isinstance(obj, ConsultaMedica):
            if Tratamiento.objects.filter(consulta=obj).exists():
                reasons.append("Tiene tratamientos asociados.")
        if isinstance(obj, Tratamiento):
            if RecetaMedica.objects.filter(tratamiento=obj).exists():
                reasons.append("Tiene recetas asociadas.")
        if isinstance(obj, Medicamento):
            if RecetaMedica.objects.filter(medicamento=obj).exists():
                reasons.append("Está referenciado por recetas médicas.")
        if isinstance(obj, SeguroSalud):
            if PacienteSeguro.objects.filter(seguro=obj).exists():
                reasons.append("Tiene afiliaciones de pacientes.")
        return reasons

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        reasons = self.related_reasons(obj)
        if reasons:
            ctx["cannot_delete_reason"] = " ".join(reasons)
        if self.cancel_url_name:
            ctx["cancel_url"] = reverse(self.cancel_url_name)
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            reasons = " ".join(self.related_reasons(self.object)) or "Existen registros relacionados."
            messages.error(request, f"No se puede eliminar «{self.object}». {reasons}")
            return redirect(self.get_success_url())


# ---------- PACIENTES ----------
class PacienteList(PageNamesMixin, ListView):
    model = Paciente
    template_name = "clinica/pacientes_list.html"
    page_update_name = "paciente_update"
    page_delete_name = "paciente_delete"

class PacienteCreate(FormExtrasMixin, CreateView):
    model = Paciente
    fields = "__all__"
    template_name = "clinica/paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    page_title = "Nuevo Paciente"
    cancel_url_name = "paciente_list"

class PacienteUpdate(FormExtrasMixin, UpdateView):
    model = Paciente
    fields = "__all__"
    template_name = "clinica/paciente_form.html"
    success_url = reverse_lazy("paciente_list")
    page_title = "Editar Paciente"
    cancel_url_name = "paciente_list"

class PacienteDelete(SafeDeleteMixin, DeleteView):
    model = Paciente
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("paciente_list")
    cancel_url_name = "paciente_list"


# ---------- MÉDICOS ----------
class MedicoList(PageNamesMixin, ListView):
    model = Medico
    template_name = "clinica/medicos_list.html"
    page_update_name = "medico_update"
    page_delete_name = "medico_delete"

class MedicoCreate(FormExtrasMixin, CreateView):
    model = Medico
    fields = "__all__"
    template_name = "clinica/medico_form.html"
    success_url = reverse_lazy("medico_list")
    page_title = "Nuevo Médico"
    cancel_url_name = "medico_list"

class MedicoUpdate(FormExtrasMixin, UpdateView):
    model = Medico
    fields = "__all__"
    template_name = "clinica/medico_form.html"
    success_url = reverse_lazy("medico_list")
    page_title = "Editar Médico"
    cancel_url_name = "medico_list"

class MedicoDelete(SafeDeleteMixin, DeleteView):
    model = Medico
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("medico_list")
    cancel_url_name = "medico_list"


# ---------- ESPECIALIDADES ----------
class EspecialidadList(PageNamesMixin, ListView):
    model = Especialidad
    template_name = "clinica/especialidades_list.html"
    page_update_name = "especialidad_update"
    page_delete_name = "especialidad_delete"

class EspecialidadCreate(FormExtrasMixin, CreateView):
    model = Especialidad
    fields = "__all__"
    template_name = "clinica/especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")
    page_title = "Nueva Especialidad"
    cancel_url_name = "especialidad_list"

class EspecialidadUpdate(FormExtrasMixin, UpdateView):
    model = Especialidad
    fields = "__all__"
    template_name = "clinica/especialidad_form.html"
    success_url = reverse_lazy("especialidad_list")
    page_title = "Editar Especialidad"
    cancel_url_name = "especialidad_list"

class EspecialidadDelete(SafeDeleteMixin, DeleteView):
    model = Especialidad
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("especialidad_list")
    cancel_url_name = "especialidad_list"


# ---------- CONSULTAS ----------
class ConsultaList(PageNamesMixin, ListView):
    model = ConsultaMedica
    template_name = "clinica/consultas_list.html"
    page_update_name = "consulta_update"
    page_delete_name = "consulta_delete"

class ConsultaCreate(FormExtrasMixin, CreateView):
    model = ConsultaMedica
    fields = "__all__"
    template_name = "clinica/consulta_form.html"
    success_url = reverse_lazy("consulta_list")
    page_title = "Nueva Consulta"
    cancel_url_name = "consulta_list"

class ConsultaUpdate(FormExtrasMixin, UpdateView):
    model = ConsultaMedica
    fields = "__all__"
    template_name = "clinica/consulta_form.html"
    success_url = reverse_lazy("consulta_list")
    page_title = "Editar Consulta"
    cancel_url_name = "consulta_list"

class ConsultaDelete(SafeDeleteMixin, DeleteView):
    model = ConsultaMedica
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("consulta_list")
    cancel_url_name = "consulta_list"


# ---------- TRATAMIENTOS ----------
class TratamientoList(PageNamesMixin, ListView):
    model = Tratamiento
    template_name = "clinica/tratamientos_list.html"
    page_update_name = "tratamiento_update"
    page_delete_name = "tratamiento_delete"

class TratamientoCreate(FormExtrasMixin, CreateView):
    model = Tratamiento
    fields = "__all__"
    template_name = "clinica/tratamiento_form.html"
    success_url = reverse_lazy("tratamiento_list")
    page_title = "Nuevo Tratamiento"
    cancel_url_name = "tratamiento_list"

class TratamientoUpdate(FormExtrasMixin, UpdateView):
    model = Tratamiento
    fields = "__all__"
    template_name = "clinica/tratamiento_form.html"
    success_url = reverse_lazy("tratamiento_list")
    page_title = "Editar Tratamiento"
    cancel_url_name = "tratamiento_list"

class TratamientoDelete(SafeDeleteMixin, DeleteView):
    model = Tratamiento
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("tratamiento_list")
    cancel_url_name = "tratamiento_list"


# ---------- MEDICAMENTOS ----------
class MedicamentoList(PageNamesMixin, ListView):
    model = Medicamento
    template_name = "clinica/medicamentos_list.html"
    page_update_name = "medicamento_update"
    page_delete_name = "medicamento_delete"

class MedicamentoCreate(FormExtrasMixin, CreateView):
    model = Medicamento
    fields = "__all__"
    template_name = "clinica/medicamento_form.html"
    success_url = reverse_lazy("medicamento_list")
    page_title = "Nuevo Medicamento"
    cancel_url_name = "medicamento_list"

class MedicamentoUpdate(FormExtrasMixin, UpdateView):
    model = Medicamento
    fields = "__all__"
    template_name = "clinica/medicamento_form.html"
    success_url = reverse_lazy("medicamento_list")
    page_title = "Editar Medicamento"
    cancel_url_name = "medicamento_list"

class MedicamentoDelete(SafeDeleteMixin, DeleteView):
    model = Medicamento
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("medicamento_list")
    cancel_url_name = "medicamento_list"


# ---------- RECETAS ----------
class RecetaList(PageNamesMixin, ListView):
    model = RecetaMedica
    template_name = "clinica/recetas_list.html"
    page_update_name = "receta_update"
    page_delete_name = "receta_delete"

class RecetaCreate(FormExtrasMixin, CreateView):
    model = RecetaMedica
    fields = "__all__"
    template_name = "clinica/receta_form.html"
    success_url = reverse_lazy("receta_list")
    page_title = "Nueva Receta"
    cancel_url_name = "receta_list"

class RecetaUpdate(FormExtrasMixin, UpdateView):
    model = RecetaMedica
    fields = "__all__"
    template_name = "clinica/receta_form.html"
    success_url = reverse_lazy("receta_list")
    page_title = "Editar Receta"
    cancel_url_name = "receta_list"

class RecetaDelete(SafeDeleteMixin, DeleteView):
    model = RecetaMedica
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("receta_list")
    cancel_url_name = "receta_list"


# ---------- SEGUROS ----------
class SeguroList(PageNamesMixin, ListView):
    model = SeguroSalud
    template_name = "clinica/seguros_list.html"
    page_update_name = "seguro_update"
    page_delete_name = "seguro_delete"

class SeguroCreate(FormExtrasMixin, CreateView):
    model = SeguroSalud
    fields = "__all__"
    template_name = "clinica/seguro_form.html"
    success_url = reverse_lazy("seguro_list")
    page_title = "Nuevo Seguro"
    cancel_url_name = "seguro_list"

class SeguroUpdate(FormExtrasMixin, UpdateView):
    model = SeguroSalud
    fields = "__all__"
    template_name = "clinica/seguro_form.html"
    success_url = reverse_lazy("seguro_list")
    page_title = "Editar Seguro"
    cancel_url_name = "seguro_list"

class SeguroDelete(SafeDeleteMixin, DeleteView):
    model = SeguroSalud
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("seguro_list")
    cancel_url_name = "seguro_list"


# ---------- AFILIACIONES PACIENTE–SEGURO ----------
class PacienteSeguroList(PageNamesMixin, ListView):
    model = PacienteSeguro
    template_name = "clinica/paciente_seguros_list.html"
    page_update_name = "paciente_seguro_update"
    page_delete_name = "paciente_seguro_delete"

class PacienteSeguroCreate(FormExtrasMixin, CreateView):
    model = PacienteSeguro
    fields = "__all__"
    template_name = "clinica/paciente_seguro_form.html"
    success_url = reverse_lazy("paciente_seguro_list")
    page_title = "Nueva Afiliación"
    cancel_url_name = "paciente_seguro_list"

class PacienteSeguroUpdate(FormExtrasMixin, UpdateView):
    model = PacienteSeguro
    fields = "__all__"
    template_name = "clinica/paciente_seguro_form.html"
    success_url = reverse_lazy("paciente_seguro_list")
    page_title = "Editar Afiliación"
    cancel_url_name = "paciente_seguro_list"

class PacienteSeguroDelete(SafeDeleteMixin, DeleteView):
    model = PacienteSeguro
    template_name = "clinica/confirm_delete.html"
    success_url = reverse_lazy("paciente_seguro_list")
    cancel_url_name = "paciente_seguro_list"