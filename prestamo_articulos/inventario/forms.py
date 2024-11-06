# forms.py
from django import forms
from .models import Articulo, Prestamo, Departamento

class SolicitarPrestamoForm(forms.Form):
    nombre_persona = forms.CharField(label='Nombre del Solicitante', max_length=100)
    cargo_persona = forms.CharField(label='Cargo del Solicitante', max_length=100)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.all(), label='Departamento', required=True)
    fecha_solicitud = forms.DateField(label='Fecha de Solicitud')
    fecha_devolucion = forms.DateField(label='Fecha de Devolución')
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), label='Artículo Disponible')

    def clean(self):
        cleaned_data = super().clean()
        fecha_solicitud = cleaned_data.get('fecha_solicitud')
        fecha_devolucion = cleaned_data.get('fecha_devolucion')
        articulo = cleaned_data.get('articulo')

        if Prestamo.objects.filter(articulo=articulo, devuelto=False).filter(
            fecha_solicitud__lt=fecha_devolucion,
            fecha_devolucion__gt=fecha_solicitud
        ).exists():
            raise forms.ValidationError("El artículo no está disponible en las fechas seleccionadas.")

        return cleaned_data

