# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .forms import SolicitarPrestamoForm
from .models import Articulo,Prestamo
from django.utils import timezone
from django.contrib import messages  # Importar mensajes
from django.contrib.auth.decorators import login_required
from datetime import date
from datetime import datetime
import pytz
from datetime import date, timedelta



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
        hoy_utc = timezone.now()  # Obtiene la fecha y hora actual en UTC
        hoy_local = timezone.localtime(hoy_utc)  # Convierte a la hora local
        hoy_date = hoy_local.date()  # Obtiene solo la fecha

        if filtro == 'hoy':
            prestamos = prestamos.filter(fecha_devolucion=hoy_date)  # Filtrar por devoluciones de hoy
        elif filtro == 'otras':
            prestamos = prestamos.exclude(fecha_devolucion=hoy_date)  # Excluir devoluciones de hoy

    # Imprimir la consulta SQL generada
    print(prestamos.query)  # Agrega esta línea para ver la consulta SQL generada

    return render(request, 'inventario/devolver_articulo.html', {'prestamos': prestamos})


@login_required
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
    hoy_str = hoy.isoformat()
    max_fecha_solicitud = (hoy + timedelta(days=5)).isoformat()  # Fecha máxima para la solicitud (5 días desde hoy)
    
    articulos = []
    mostrar_tabla = False

    # Validación de fechas si se seleccionaron
    if fecha_solicitud:
        fecha_solicitud_obj = date.fromisoformat(fecha_solicitud)
        max_fecha_devolucion = (fecha_solicitud_obj + timedelta(days=7)).isoformat()  # Fecha máxima de devolución (7 días desde la solicitud)

        if fecha_solicitud_obj > hoy + timedelta(days=5):
            messages.error(request, "No se pueden realizar préstamos a más de 5 días desde la fecha actual.")
        elif fecha_devolucion:
            fecha_devolucion_obj = date.fromisoformat(fecha_devolucion)
            if fecha_devolucion_obj > fecha_solicitud_obj + timedelta(days=7):
                messages.error(request, "La fecha de devolución no puede ser más de 7 días después de la fecha de solicitud.")
            else:
                # Excluir los artículos que ya tienen un préstamo en el rango seleccionado
                articulos_prestados = Prestamo.objects.filter(
                    devuelto=False,
                    fecha_solicitud__lte=fecha_devolucion_obj,
                    fecha_devolucion__gte=fecha_solicitud_obj
                ).values_list('articulo_id', flat=True)

                # Obtener los artículos que no están prestados en ese rango de fechas
                articulos = Articulo.objects.exclude(id__in=articulos_prestados)
                mostrar_tabla = True
    else:
        max_fecha_devolucion = max_fecha_solicitud

    return render(request, 'inventario/disponibilidad.html', {
        'articulos': articulos,
        'hoy': hoy_str,
        'mostrar_tabla': mostrar_tabla,
        'max_fecha_solicitud': max_fecha_solicitud,
        'max_fecha_devolucion': max_fecha_devolucion  # Fecha máxima para devolución dinámica
    })
@login_required
def equipos_a_entregar_hoy(request):
    hoy = timezone.now().date()  # Obtén la fecha actual
    prestamos_a_entregar = Prestamo.objects.filter(fecha_solicitud=hoy, entregado=False)

    return render(request, 'inventario/equipos_a_entregar.html', {
        'prestamos_a_entregar': prestamos_a_entregar,
    })
@login_required
def marcar_como_entregado(request, prestamo_id):
    prestamo = get_object_or_404(Prestamo, id=prestamo_id)
    prestamo.entregado = True  # Marcamos como entregado
    prestamo.save()
    return redirect('equipos_a_entregar_hoy')  # Redirigir a la lista de equipos a entregar
@login_required
def admin_panel(request):
    return render(request, 'inventario/admin_panel.html')

