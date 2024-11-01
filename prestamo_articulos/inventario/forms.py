# inventario/forms.py
from django import forms
from .models import Articulo

class SolicitarPrestamoForm(forms.Form):
    nombre_persona = forms.CharField(label='Nombre del Solicitante', max_length=100)
    cargo_persona = forms.CharField(label='Cargo del Solicitante', max_length=100)
    fecha_solicitud = forms.DateField(label='Fecha de Solicitud')
    fecha_devolucion = forms.DateField(label='Fecha de Devolución')
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.filter(prestado=False), label='Artículo Disponible')

    def clean(self):
        cleaned_data = super().clean()
        fecha_devolucion = cleaned_data.get('fecha_devolucion')
        articulo = cleaned_data.get('articulo')

        # Validación de disponibilidad del artículo en las fechas
        if articulo.prestado:
            raise forms.ValidationError("El artículo ya está prestado.")

        return cleaned_data
