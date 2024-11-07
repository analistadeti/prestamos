from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_view

urlpatterns = [
    path('', views.disponibilidad_articulos, name='disponibilidad'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('accounts/', include('django.contrib.auth.urls')),  # Agrega esta línea
    path('solicitar_prestamo/', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('guardar_prestamo/', views.guardar_prestamo, name='guardar_prestamo'),
    path('devolver_articulo/', views.devolver_articulo, name='devolver_articulo'),
    path('confirmar_devolucion/<int:prestamo_id>/', views.confirmar_devolucion, name='confirmar_devolucion'),
    path('equipos-a-entregar-hoy/', views.equipos_a_entregar_hoy, name='equipos_a_entregar_hoy'),
    path('marcar-como-entregado/<int:prestamo_id>/', views.marcar_como_entregado, name='marcar_como_entregado'),
    path('equipos_en_bodega/', views.equipos_en_bodega, name='equipos_en_bodega'),
    path('inventario/', views.inventario, name='inventario'),
    path('logout/', logout_view, name='logout'),

]
