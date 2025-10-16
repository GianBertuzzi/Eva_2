from django.db import models

# ---------- CHOICES ----------
TIPO_SANGRE_CHOICES = [
    ("O+", "O+"), ("O-", "O-"),
    ("A+", "A+"), ("A-", "A-"),
    ("B+", "B+"), ("B-", "B-"),
    ("AB+", "AB+"), ("AB-", "AB-"),
]

SEXO_CHOICES = [
    ("M", "Masculino"),
    ("F", "Femenino"),
    ("X", "No especificado"),
]

ESTADO_CONSULTA_CHOICES = [
    ("PEND", "Pendiente"),
    ("ATEN", "Atendida"),
    ("CANC", "Cancelada"),
    ("NOAS", "No asiste"),
]

# ---------- MODELOS BASE ----------
class Especialidad(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    descripcion = models.TextField(blank=True)
    def __str__(self): return self.nombre

class Medico(models.Model):
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField()
    telefono = models.CharField(max_length=30, blank=True)
    activo = models.BooleanField(default=True)
    # PROTECT: no se puede borrar una especialidad si tiene médicos
    especialidad = models.ForeignKey(Especialidad, on_delete=models.PROTECT, related_name='medicos')
    def __str__(self): return f"{self.nombre} {self.apellido}"

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=120)
    apellido = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, default='X')
    tipo_sangre = models.CharField(max_length=3, choices=TIPO_SANGRE_CHOICES, blank=True)
    correo = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    activo = models.BooleanField(default=True)
    def __str__(self): return f"{self.nombre} {self.apellido}"

class ConsultaMedica(models.Model):
    # PROTECT: no se puede borrar paciente/médico si hay consultas
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, related_name='consultas')
    medico = models.ForeignKey(Medico, on_delete=models.PROTECT, related_name='consultas')
    fecha_consulta = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    diagnostico = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=4, choices=ESTADO_CONSULTA_CHOICES, default='PEND')
    def __str__(self): return f"Consulta {self.id} - {self.paciente}"

class Tratamiento(models.Model):
    # PROTECT: no se puede borrar la consulta si tiene tratamientos
    consulta = models.ForeignKey(ConsultaMedica, on_delete=models.PROTECT, related_name='tratamientos')
    descripcion = models.TextField()
    duracion_dias = models.PositiveIntegerField(default=0)
    observaciones = models.TextField(blank=True)
    def __str__(self): return f"Tratamiento {self.id}"

class Medicamento(models.Model):
    nombre = models.CharField(max_length=120)
    laboratorio = models.CharField(max_length=120, blank=True)
    stock = models.PositiveIntegerField(default=0)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return self.nombre

class RecetaMedica(models.Model):
    # PROTECT: no se puede borrar tratamiento/medicamento si hay recetas
    tratamiento = models.ForeignKey(Tratamiento, on_delete=models.PROTECT, related_name='recetas')
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT, related_name='recetas')
    dosis = models.CharField(max_length=60)        # ej: "500 mg"
    frecuencia = models.CharField(max_length=60)   # ej: "cada 8 horas"
    duracion = models.CharField(max_length=60)     # ej: "7 días"
    def __str__(self): return f"Receta {self.id} - {self.medicamento}"

# ---------- NUEVAS TABLAS: Seguros ----------
class SeguroSalud(models.Model):
    """Catálogo de seguros: Fonasa/Isapre y su plan."""
    nombre = models.CharField(max_length=120)        # p.ej. Fonasa / Colmena
    plan = models.CharField(max_length=120, blank=True)  # p.ej. B / Oro
    class Meta:
        unique_together = ('nombre', 'plan')         # evita duplicados exactos
    def __str__(self): return f"{self.nombre} {self.plan}".strip()

class PacienteSeguro(models.Model):
    """Relación Paciente–Seguro con datos propios de afiliación."""
    # CASCADE: al borrar paciente, se borran sus afiliaciones
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='seguros')
    # PROTECT: no se puede borrar un seguro con afiliados
    seguro = models.ForeignKey(SeguroSalud, on_delete=models.PROTECT, related_name='afiliados')
    nro_poliza = models.CharField(max_length=60, blank=True)
    cobertura_porcentaje = models.PositiveIntegerField(default=0)  # 0..100
    vigente = models.BooleanField(default=True)
    class Meta:
        unique_together = ('paciente', 'seguro')
    def __str__(self): return f"{self.paciente} - {self.seguro}"