from django.contrib import admin
from .models import CategoriaEvento, Usuario, Evento, Inscripcion

admin.site.register(CategoriaEvento)
admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(Inscripcion)