from django import forms
from .models import CategoriaEvento, Usuario, Evento, Inscripcion


class CategoriaEventoForm(forms.ModelForm):
    class Meta:
        model = CategoriaEvento
        fields = ['codigo_categoria', 'nombre', 'descripcion']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['dni', 'nombre', 'apellidos', 'email', 'telefono', 'tipo_usuario']


class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = [
            'codigo_evento',
            'titulo',
            'descripcion',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'ubicacion',
            'aforo_maximo',
            'estado',
            'categoria'
        ]


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = [
            'codigo_inscripcion',
            'fecha_inscripcion',
            'estado',
            'usuario',
            'evento',
            'confirmacion_asistencia'
        ]