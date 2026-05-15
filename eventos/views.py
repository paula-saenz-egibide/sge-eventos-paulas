from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Evento, Inscripcion, Usuario, CategoriaEvento
from .forms import EventoForm, InscripcionForm, UsuarioForm
from .serializers import (
    EventoSerializer,
    EventoCreateUpdateSerializer,
    UsuarioSerializer,
    InscripcionSerializer,
    InscripcionCreateUpdateSerializer,
    CategoriaEventoSerializer,
)


# =========================
# CRUD EVENTOS HTML
# =========================

def listar_eventos(request):
    eventos = Evento.objects.all()

    return render(request, 'eventos/listar_eventos.html', {
        'eventos': eventos
    })


def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()

    return render(request, 'eventos/crear_evento.html', {
        'form': form
    })


def ver_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)

    return render(request, 'eventos/ver_evento.html', {
        'evento': evento
    })


def editar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)

        if form.is_valid():
            form.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm(instance=evento)

    return render(request, 'eventos/editar_evento.html', {
        'form': form,
        'evento': evento
    })


def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)

    if request.method == 'POST':
        evento.delete()
        return redirect('listar_eventos')

    return render(request, 'eventos/eliminar_evento.html', {
        'evento': evento
    })


# =========================
# CRUD INSCRIPCIONES HTML
# =========================

def listar_inscripciones(request):
    inscripciones = Inscripcion.objects.all()

    return render(request, 'eventos/listar_inscripciones.html', {
        'inscripciones': inscripciones
    })


def crear_inscripcion(request):
    error = None

    if request.method == 'POST':
        form = InscripcionForm(request.POST)

        if form.is_valid():
            try:
                inscripcion = form.save(commit=False)
                inscripcion.clean()
                inscripcion.save()

                return redirect('listar_inscripciones')

            except ValidationError as e:
                error = e
    else:
        form = InscripcionForm()

    return render(request, 'eventos/crear_inscripcion.html', {
        'form': form,
        'error': error
    })


def editar_inscripcion(request, inscripcion_id):
    inscripcion = Inscripcion.objects.get(id=inscripcion_id)
    error = None

    if request.method == 'POST':
        form = InscripcionForm(request.POST, instance=inscripcion)

        if form.is_valid():
            try:
                nueva_inscripcion = form.save(commit=False)
                nueva_inscripcion.clean()
                nueva_inscripcion.save()

                return redirect('listar_inscripciones')

            except ValidationError as e:
                error = e
    else:
        form = InscripcionForm(instance=inscripcion)

    return render(request, 'eventos/editar_inscripcion.html', {
        'form': form,
        'error': error,
        'inscripcion': inscripcion
    })


def cancelar_inscripcion(request, inscripcion_id):
    inscripcion = Inscripcion.objects.get(id=inscripcion_id)
    inscripcion.estado = 'CANCELADA'
    inscripcion.save()

    return redirect('listar_inscripciones')


# =========================
# CRUD USUARIOS HTML
# =========================

def listar_usuarios(request):
    usuarios = Usuario.objects.all()

    return render(request, 'eventos/listar_usuarios.html', {
        'usuarios': usuarios
    })


def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm()

    return render(request, 'eventos/crear_usuario.html', {
        'form': form
    })


def ver_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    inscripciones = Inscripcion.objects.filter(usuario=usuario)

    return render(request, 'eventos/ver_usuario.html', {
        'usuario': usuario,
        'inscripciones': inscripciones
    })


def editar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)

        if form.is_valid():
            form.save()
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'eventos/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


def eliminar_usuario(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('listar_usuarios')

    return render(request, 'eventos/eliminar_usuario.html', {
        'usuario': usuario
    })


# =========================
# API EVENTOS
# =========================

@api_view(['GET', 'POST'])
def api_lista_eventos(request):
    if request.method == 'GET':
        eventos = Evento.objects.all().order_by('fecha')
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EventoCreateUpdateSerializer(data=request.data)

        if serializer.is_valid():
            evento = serializer.save()
            serializer_respuesta = EventoSerializer(evento)
            return Response(serializer_respuesta.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def api_detalle_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)

    if request.method == 'GET':
        serializer = EventoSerializer(evento)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EventoCreateUpdateSerializer(evento, data=request.data)

        if serializer.is_valid():
            evento_actualizado = serializer.save()
            serializer_respuesta = EventoSerializer(evento_actualizado)
            return Response(serializer_respuesta.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        evento.delete()
        return Response(
            {"mensaje": "Evento eliminado correctamente"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================
# API INSCRIPCIONES
# =========================

@api_view(['GET', 'POST'])
def api_inscripciones_evento(request, evento_id):
    if request.method == 'GET':
        inscripciones = Inscripcion.objects.filter(evento_id=evento_id)
        serializer = InscripcionSerializer(inscripciones, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        data = request.data.copy()
        data['evento'] = evento_id

        usuario_id = data.get('usuario')

        # Si ya existe una inscripción cancelada para ese usuario y evento,
        # se reactiva esa misma inscripción en vez de crear una duplicada.
        inscripcion_cancelada = Inscripcion.objects.filter(
            usuario_id=usuario_id,
            evento_id=evento_id,
            estado='CANCELADA'
        ).first()

        if inscripcion_cancelada:
            inscripcion_cancelada.codigo_inscripcion = data.get(
                'codigo_inscripcion',
                inscripcion_cancelada.codigo_inscripcion
            )
            inscripcion_cancelada.fecha_inscripcion = data.get(
                'fecha_inscripcion',
                inscripcion_cancelada.fecha_inscripcion
            )
            inscripcion_cancelada.estado = data.get('estado', 'CONFIRMADA')
            inscripcion_cancelada.confirmacion_asistencia = data.get(
                'confirmacion_asistencia',
                False
            )

            try:
                inscripcion_cancelada.save()
                serializer_respuesta = InscripcionSerializer(inscripcion_cancelada)
                return Response(serializer_respuesta.data, status=status.HTTP_200_OK)

            except ValidationError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Si no existe inscripción cancelada, se crea una nueva inscripción.
        serializer = InscripcionCreateUpdateSerializer(data=data)

        if serializer.is_valid():
            try:
                inscripcion = serializer.save()
                serializer_respuesta = InscripcionSerializer(inscripcion)
                return Response(serializer_respuesta.data, status=status.HTTP_201_CREATED)

            except ValidationError as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def api_cancelar_inscripcion(request, inscripcion_id):
    inscripcion = Inscripcion.objects.get(id=inscripcion_id)
    inscripcion.estado = 'CANCELADA'
    inscripcion.save()

    serializer = InscripcionSerializer(inscripcion)
    return Response(serializer.data)


# =========================
# API USUARIOS
# =========================

@api_view(['GET'])
def api_lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('apellidos', 'nombre')
    serializer = UsuarioSerializer(usuarios, many=True)

    return Response(serializer.data)


# =========================
# API CATEGORÍAS
# =========================

@api_view(['GET'])
def api_lista_categorias(request):
    categorias = CategoriaEvento.objects.all().order_by('nombre')
    serializer = CategoriaEventoSerializer(categorias, many=True)

    return Response(serializer.data)


# =========================
# API LOGIN / USUARIO ACTUAL
# =========================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_usuario_me(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "is_staff": user.is_staff,
    })