# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import SolicitarPrestamoForm
from .models import Articulo,Prestamo
from django.utils import timezone
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.decorators import login_required
from datetime import date


def solicitar_prestamo(request):
    if request.method == 'POST':
        articulo_ids = request.POST.getlist('articulos')
        articulos = Articulo.objects.filter(id__in=articulo_ids)
        fecha_solicitud = request.POST.get('fecha_solicitud')
        fecha_devolucion = request.POST.get('fecha_devolucion')

        if articulos.exists():
            return render(request, 'inventario/solicitar_prestamo.html', {
                'articulos': articulos,
                'fecha_solicitud': fecha_solicitud,
                'fecha_devolucion': fecha_devolucion
            })

    return redirect('disponibilidad')

def guardar_prestamo(request):
    if request.method == 'POST':
        articulo_ids = request.POST.getlist('articulos')  # Obtener varios IDs
        nombre_persona = request.POST.get('nombre_persona')
        cargo_persona = request.POST.get('cargo_persona')
        fecha_solicitud = request.POST.get('fecha_solicitud')
        fecha_devolucion = request.POST.get('fecha_devolucion')

        # Convertir fechas a objetos datetime
        fecha_solicitud = timezone.datetime.strptime(fecha_solicitud, '%Y-%m-%d').date()
        fecha_devolucion = timezone.datetime.strptime(fecha_devolucion, '%Y-%m-%d').date()

        if articulo_ids and nombre_persona and cargo_persona and fecha_solicitud and fecha_devolucion:
            for articulo_id in articulo_ids:
                try:
                    # Verificar si hay préstamos existentes que se solapen con las fechas ingresadas
                    if not Prestamo.objects.filter(articulo_id=articulo_id, devuelto=False).filter(
                            fecha_devolucion__gt=fecha_solicitud,
                            fecha_solicitud__lt=fecha_devolucion).exists():
                        
                        articulo = Articulo.objects.get(id=articulo_id)

                        # Crear el préstamo
                        prestamo = Prestamo(
                            articulo=articulo,
                            nombre_persona=nombre_persona,
                            cargo_persona=cargo_persona,
                            fecha_solicitud=fecha_solicitud,
                            fecha_devolucion=fecha_devolucion,
                            devuelto=False
                        )
                        prestamo.save()
                    else:
                        messages.warning(request, f'El artículo {articulo.nombre} no está disponible en las fechas solicitadas.')

                except Articulo.DoesNotExist:
                    continue  # Si no existe el artículo, simplemente continuamos

            messages.success(request, 'Préstamo(s) exitoso(s). Puedes pasar a tecnología por el equipo en la fecha seleccionada.')
            return redirect('disponibilidad')
    
    messages.error(request, 'Error al realizar el préstamo. Por favor, verifica la información.')
    return redirect('disponibilidad')
@login_required
def devolver_articulo(request):
    prestamos = Prestamo.objects.filter(devuelto=False)  # Obtener préstamos no devueltos

    if request.method == 'GET':
        # Filtrar por nombre de artículo si se proporciona
        nombre_articulo = request.GET.get('nombre_articulo', '')
        if nombre_articulo:
            prestamos = prestamos.filter(articulo__nombre__icontains=nombre_articulo)  # Filtrar por nombre de artículo

        # Filtrar por fecha de devolución
        filtro = request.GET.get('filtro', '')
        if filtro == 'hoy':
            hoy = timezone.now().date()
            prestamos = prestamos.filter(fecha_devolucion=hoy)  # Filtrar por devoluciones de hoy
        elif filtro == 'otras':
            hoy = timezone.now().date()
            prestamos = prestamos.exclude(fecha_devolucion=hoy)  # Excluir devoluciones de hoy

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
    fecha_solicitud = request.GET.get('fecha_solicitud')
    fecha_devolucion = request.GET.get('fecha_devolucion')
    hoy = date.today()

    # Mostrar la tabla solo cuando el rango de fechas ha sido seleccionado
    articulos = []
    if fecha_solicitud and fecha_devolucion:
        articulos_prestados = Prestamo.objects.filter(
            devuelto=False,
            fecha_solicitud__lt=fecha_devolucion,
            fecha_devolucion__gt=fecha_solicitud
        ).values_list('articulo_id', flat=True)

        # Aquí excluyes los artículos que están prestados en el rango de fechas
        articulos = Articulo.objects.exclude(id__in=articulos_prestados)

    return render(request, 'inventario/disponibilidad.html', {
        'articulos': articulos,
        'hoy': hoy,
        'mostrar_tabla': bool(fecha_solicitud and fecha_devolucion),  # Variable de control para la tabla
    })
@login_required
def admin_panel(request):
    return render(request, 'inventario/admin_panel.html')

