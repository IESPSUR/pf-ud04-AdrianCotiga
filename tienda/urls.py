from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/admin/listado/', views.listado, name='listado'),
    path('/tienda/admin/edicion/<int:pk>/', views.edicion, name='edicion'),
    path('tienda/admin/eliminar/<int:pk>/', views.eliminar, name='eliminar'),
    path('tienda/admin/nuevo/', views.nuevo, name='nuevo'),
    path('tienda/compra', views.compra, name='compra'),
    path('tienda/checkout/<int:pk>/', views.checkout, name='checkout'),
    path('tienda/informes', views.informes, name='informes'),
]
