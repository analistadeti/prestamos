from django.contrib import admin
from .models import Articulo,Prestamo,Departamento

@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('articulo', 'nombre_persona', 'entregado', 'entregado_por', 'devuelto', 'devuelto_por', 'fecha_solicitud', 'fecha_devolucion')
    list_filter = ('entregado', 'devuelto', 'entregado_por', 'devuelto_por')

admin.site.register(Articulo)
admin.site.register(Departamento)