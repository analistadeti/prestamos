from django.contrib.auth.models import User
from django.db import models

class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Articulo(models.Model): 
    nombre = models.CharField(max_length=100)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=100)
    cargo_persona = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_solicitud = models.DateField()
    fecha_devolucion = models.DateField()
    devuelto = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    # Nuevos campos para registrar quién marcó los estados
    entregado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestamos_entregados')
    devuelto_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='prestamos_devueltos')

    def __str__(self):
        return f"{self.articulo.nombre} - {self.nombre_persona}"




