from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from .models import Evento, Inscripcion, Usuario
from .forms import EventoForm, InscripcionForm, UsuarioForm


# =========================
# CRUD EVENTOS
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
# CRUD INSCRIPCIONES
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
# CRUD USUARIOS
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
