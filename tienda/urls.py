from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    # path('tienda/', views.tienda_productos, name='tienda_productos'),
    path('tienda/admin/listado/', views.listado, name='listado'),
    path('/tienda/admin/detalles/<int:pk>/', views.detalles, name='detalles'),
    path('tienda/admin/edicion/', views.edicion, name='edcion'),
    path('tienda/admin/eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('tienda/admin/nuevo/', views.nuevo, name='nuevo'),
    #path('tienda/admin/checkout/<int:pk>/', views.checkout, name='checkout')
]
