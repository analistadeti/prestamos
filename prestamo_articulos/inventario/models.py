from django.db import models


class Articulo(models.Model): 
    nombre = models.CharField(max_length=100)  # Por ejemplo, 'LT03-2018'
    observacion = models.TextField(blank=True, null=True)  # Campo de observación

    def __str__(self):
        return self.nombre


class Prestamo(models.Model):
    # La clave foránea se vincula al id de Articulo automáticamente
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    nombre_persona = models.CharField(max_length=100)
    cargo_persona = models.CharField(max_length=100)
    fecha_solicitud = models.DateField()
    fecha_devolucion = models.DateField()
    devuelto = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.articulo.nombre} - {self.nombre_persona}"



