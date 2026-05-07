from django.db import models
from django.core.exceptions import ValidationError


class CategoriaEvento(models.Model):
    codigo_categoria = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return f"{self.nombre}"


class Usuario(models.Model):
    TIPOS_USUARIO = [
        ('ALUMNO', 'Alumno'),
        ('PROFESOR', 'Profesor'),
        ('INVITADO', 'Invitado'),
        ('OTRO', 'Otro'),
    ]

    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    tipo_usuario = models.CharField(max_length=20, choices=TIPOS_USUARIO)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.dni})"


class Evento(models.Model):
    ESTADOS_EVENTO = [
        ('ABIERTO', 'Abierto'),
        ('CERRADO', 'Cerrado'),
        ('CANCELADO', 'Cancelado'),
        ('FINALIZADO', 'Finalizado'),
    ]

    codigo_evento = models.CharField(max_length=20, unique=True)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    ubicacion = models.CharField(max_length=150)
    aforo_maximo = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS_EVENTO, default='ABIERTO')
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    def __str__(self):
        return f"{self.titulo} - {self.fecha}"

    def plazas_ocupadas(self):
        return self.inscripcion_set.filter(estado='CONFIRMADA').count()

    def plazas_disponibles(self):
        return self.aforo_maximo - self.plazas_ocupadas()

    def clean(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValidationError("La hora de fin debe ser posterior a la hora de inicio.")


class Inscripcion(models.Model):
    ESTADOS_INSCRIPCION = [
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('LISTA_ESPERA', 'Lista de espera'),
    ]

    codigo_inscripcion = models.CharField(max_length=20, unique=True)
    fecha_inscripcion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS_INSCRIPCION, default='CONFIRMADA')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    confirmacion_asistencia = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='unique_usuario_evento')
        ]

    def __str__(self):
        return f"{self.codigo_inscripcion} - {self.usuario} - {self.evento}"

    def clean(self):

        # Evitar inscripciones duplicadas
        if Inscripcion.objects.filter(
                usuario=self.usuario,
                evento=self.evento
        ).exclude(id=self.id).exists():
            raise ValidationError(
                "Este usuario ya está inscrito en este evento."
            )

        # Control de aforo
        if self.estado == 'CONFIRMADA':

            if self.evento.plazas_disponibles() <= 0:
                self.estado = 'LISTA_ESPERA'

    def save(self, *args, **kwargs):

        self.clean()

        super().save(*args, **kwargs)