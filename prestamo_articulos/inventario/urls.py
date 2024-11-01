from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.disponibilidad_articulos, name='disponibilidad'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('accounts/', include('django.contrib.auth.urls')),  # Agrega esta línea
    path('solicitar_prestamo/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('guardar_prestamo/', views.guardar_prestamo, name='guardar_prestamo'),
    path('devolver_articulo/', views.devolver_articulo, name='devolver_articulo'),
    path('confirmar_devolucion/<int:prestamo_id>/', views.confirmar_devolucion, name='confirmar_devolucion'),

]
