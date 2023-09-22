from django.contrib import admin
from .models import Empleados

# Register your models here.

class Empleadosadmin(admin.ModelAdmin):
    list_display = ('id','Nombre','Apellidos','Celular','Correo','hora_inicio', 'hora_fin')
    search_fields = ('Nombre', 'Apellidos')
    ordering = ('IDempleado')


admin.site.register(Empleados, Empleadosadmin)
