from django.urls import path

from .views import (
    listar_eventos,
    crear_evento,
    ver_evento,
    editar_evento,
    eliminar_evento,

    listar_inscripciones,
    crear_inscripcion,
    editar_inscripcion,
    cancelar_inscripcion,

    listar_usuarios,
    crear_usuario,
    ver_usuario,
    editar_usuario,
    eliminar_usuario
)

urlpatterns = [

    # =========================
    # EVENTOS
    # =========================

    path(
        'eventos/',
        listar_eventos,
        name='listar_eventos'
    ),

    path(
        'eventos/crear/',
        crear_evento,
        name='crear_evento'
    ),

    path(
        'eventos/<int:evento_id>/',
        ver_evento,
        name='ver_evento'
    ),

    path(
        'eventos/editar/<int:evento_id>/',
        editar_evento,
        name='editar_evento'
    ),

    path(
        'eventos/eliminar/<int:evento_id>/',
        eliminar_evento,
        name='eliminar_evento'
    ),


    # =========================
    # INSCRIPCIONES
    # =========================

    path(
        'inscripciones/',
        listar_inscripciones,
        name='listar_inscripciones'
    ),

    path(
        'inscripciones/crear/',
        crear_inscripcion,
        name='crear_inscripcion'
    ),

    path(
        'inscripciones/editar/<int:inscripcion_id>/',
        editar_inscripcion,
        name='editar_inscripcion'
    ),

    path(
        'inscripciones/cancelar/<int:inscripcion_id>/',
        cancelar_inscripcion,
        name='cancelar_inscripcion'
    ),


    # =========================
    # USUARIOS
    # =========================

    path(
        'usuarios/',
        listar_usuarios,
        name='listar_usuarios'
    ),

    path(
        'usuarios/crear/',
        crear_usuario,
        name='crear_usuario'
    ),

    path(
        'usuarios/<int:usuario_id>/',
        ver_usuario,
        name='ver_usuario'
    ),

    path(
        'usuarios/editar/<int:usuario_id>/',
        editar_usuario,
        name='editar_usuario'
    ),

    path(
        'usuarios/eliminar/<int:usuario_id>/',
        eliminar_usuario,
        name='eliminar_usuario'
    ),
]