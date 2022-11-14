from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('tienda/', views.welcome, name='welcome'),
    path('tienda/admin/listado/', views.listado, name='listado'),
    path('/tienda/admin/detalles/<int:pk>/', views.detalles, name='detalles'),
    path('tienda/admin/edicion/', views.edicion, name='edcion'),
    path('tienda/admin/eliminar/', views.eliminar, name='eliminar'),
    path('tienda/admin/nuevo/<int:pk>/', views.nuevo, name='nuevo'),
]
