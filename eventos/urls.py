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
    eliminar_usuario,

    api_lista_eventos,
    api_detalle_evento,
    api_inscripciones_evento,
    api_lista_usuarios,
    api_detalle_usuario,
    api_lista_categorias,
    api_usuario_me,
    api_cancelar_inscripcion,
    api_toggle_asistencia_inscripcion,
)

urlpatterns = [

    # EVENTOS HTML

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

    # INSCRIPCIONES HTML

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

    # USUARIOS HTML

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

    # API EVENTOS

    path(
        'api/eventos/',
        api_lista_eventos,
        name='api_lista_eventos'
    ),

    path(
        'api/eventos/<int:evento_id>/',
        api_detalle_evento,
        name='api_detalle_evento'
    ),

    path(
        'api/eventos/<int:evento_id>/inscripciones/',
        api_inscripciones_evento,
        name='api_inscripciones_evento'
    ),

    # API USUARIOS

    path(
        'api/usuarios/',
        api_lista_usuarios,
        name='api_lista_usuarios'
    ),

    path(
        'api/usuarios/me/',
        api_usuario_me,
        name='api_usuario_me'
    ),

    path(
        'api/usuarios/<str:dni>/',
        api_detalle_usuario,
        name='api_detalle_usuario'
    ),

    # API CATEGORÍAS

    path(
        'api/categorias/',
        api_lista_categorias,
        name='api_lista_categorias'
    ),

    # API INSCRIPCIONES

    path(
        'api/inscripciones/<int:inscripcion_id>/cancelar/',
        api_cancelar_inscripcion,
        name='api_cancelar_inscripcion'
    ),

    path(
        'api/inscripciones/<int:inscripcion_id>/asistencia/',
        api_toggle_asistencia_inscripcion,
        name='api_toggle_asistencia_inscripcion'
    ),
]