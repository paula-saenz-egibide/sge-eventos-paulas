from rest_framework import serializers
from .models import Evento, Usuario, Inscripcion, CategoriaEvento


class CategoriaEventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaEvento
        fields = [
            'id',
            'codigo_categoria',
            'nombre',
            'descripcion',
        ]


class EventoSerializer(serializers.ModelSerializer):
    categoria = CategoriaEventoSerializer()

    class Meta:
        model = Evento
        fields = [
            'id',
            'codigo_evento',
            'titulo',
            'descripcion',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'ubicacion',
            'aforo_maximo',
            'estado',
            'categoria',
        ]


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'dni',
            'nombre',
            'apellidos',
            'email',
            'telefono',
            'tipo_usuario',
        ]


class InscripcionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    evento = EventoSerializer()

    class Meta:
        model = Inscripcion
        fields = [
            'id',
            'codigo_inscripcion',
            'fecha_inscripcion',
            'estado',
            'usuario',
            'evento',
            'confirmacion_asistencia',
        ]
