# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import SolicitarPrestamoForm
from .models import Articulo,Prestamo
from django.utils import timezone
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.decorators import login_required


def solicitar_prestamo(request):
    if request.method == 'POST':
        articulo_ids = request.POST.getlist('articulos')  # Obtener lista de IDs de artículos seleccionados
        articulos = Articulo.objects.filter(id__in=articulo_ids)  # Filtrar artículos seleccionados

        if articulos.exists():
            return render(request, 'inventario/solicitar_prestamo.html', {'articulos': articulos})

    return redirect('disponibilidad')

def guardar_prestamo(request):
    if request.method == 'POST':
        articulo_ids = request.POST.get('articulo_ids', '')
        if articulo_ids:
            articulo_ids = articulo_ids.split(',')
            nombre_persona = request.POST['nombre_persona']
            cargo_persona = request.POST['cargo_persona']
            fecha_solicitud = request.POST['fecha_solicitud']
            fecha_devolucion = request.POST['fecha_devolucion']

            for articulo_id in articulo_ids:
                try:
                    articulo = Articulo.objects.get(id=int(articulo_id), prestado=False)
                    prestamo = Prestamo(
                        articulo=articulo,
                        nombre_persona=nombre_persona,
                        cargo_persona=cargo_persona,
                        fecha_solicitud=fecha_solicitud,
                        fecha_devolucion=fecha_devolucion,
                        devuelto=False
                    )
                    prestamo.save()
                    articulo.prestado = True
                    articulo.save()
                except Articulo.DoesNotExist:
                    continue
            
            # Guardar un mensaje de éxito
            messages.success(request, 'Préstamo exitoso. Puedes pasar a tecnología por el equipo.')
            return redirect('disponibilidad')  # Redirigir a la disponibilidad

    return redirect('disponibilidad')



@login_required
def devolver_articulo(request):
    prestamos = Prestamo.objects.filter(devuelto=False)  # Obtener préstamos no devueltos

    if request.method == 'GET':
        nombre_articulo = request.GET.get('nombre_articulo', '')
        if nombre_articulo:
            prestamos = prestamos.filter(articulo__nombre__icontains=nombre_articulo)  # Filtrar por nombre de artículo

    return render(request, 'inventario/devolver_articulo.html', {'prestamos': prestamos})

def confirmar_devolucion(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)

    if request.method == 'POST':
        # Marcar el artículo como disponible
        prestamo.articulo.prestado = False
        prestamo.articulo.save()
        # Marcar el préstamo como devuelto
        prestamo.devuelto = True
        prestamo.save()
        return redirect('devolver_articulo')  # Redirigir a la página de devolución

    return render(request, 'inventario/confirmar_devolucion.html', {'prestamo': prestamo})


def disponibilidad_articulos(request):
    articulos = Articulo.objects.filter(prestado=False)  # Solo mostrar artículos disponibles
    return render(request, 'inventario/disponibilidad.html', {'articulos': articulos})
@login_required
def admin_panel(request):
    return render(request, 'inventario/admin_panel.html')

