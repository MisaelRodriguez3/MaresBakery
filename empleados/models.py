from django.db import models

# Create your models here.
class Empleados(models.Model):
    IDempleado = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    Apellidos = models.CharField(max_length=255)
    Celular = models.CharField(max_length=20)
    Correo = models.EmailField(max_length=254, unique=True)
    Horario_inicio = models.TimeField(default='00:00')
    Horario_fin = models.TimeField(default='00:00')

    def id(self):
        return self.IDempleado

    def hora_inicio (self):
        return self.Horario_inicio
    
    def hora_fin(self):
        return self.Horario_fin
    
    id.short_description = 'ID del empleado'
    hora_inicio.short_description = 'Hora de entrada'
    hora_fin.short_description = 'Hora de salida'

    class Meta:
        db_table = 'Empleados'