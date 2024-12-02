from django.contrib import admin
from .models import User, Actividad


admin.site.register(User)

class ActividadAdmin(admin.ModelAdmin):
    # Mostrar todos los campos en la lista del admin
    list_display = ('id', 'nombre', 'descripcion', 'entrenador', 'fecha', 'hora_inicio', 'hora_fin', 'cupos', 'fecha_fin')

    # Permitir la búsqueda por campos como nombre y descripción
    search_fields = ('nombre', 'descripcion', 'entrenador__username')

    # Agregar filtros por fecha y entrenador
    list_filter = ('entrenador', 'fecha')

    # Ordenar por fecha
    ordering = ('fecha',)

# Registrar el modelo con las opciones personalizadas
admin.site.register(Actividad, ActividadAdmin)