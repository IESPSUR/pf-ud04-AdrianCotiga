from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),

    # CRUD
    path('tienda/admin/listado/', views.listado, name='listado'),
    path('tienda/admin/edicion/<int:pk>/', views.edicion, name='edicion'),
    path('tienda/admin/eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('tienda/admin/nuevo/', views.nuevo, name='nuevo'),

    # Compra
    path('tienda/compra/', views.compra, name='compra'),
    path('tienda/checkout/<int:pk>/', views.checkout, name='checkout'),

    # Informes
    path('tienda/informes/', views.informes, name='informes'),
    path('tienda/informes/productosMarca', views.productosMarca, name='productosMarca'),
    path('tienda/informes/productosVendidos', views.productosVendidos, name='productosVendidos'),
    path('tienda/informes/comprasUsuario', views.comprasUsuario, name='comprasUsuario'),
    path('tienda/informes/mejoresClientes', views.mejoresClientes, name='mejoresClientes'),
]
