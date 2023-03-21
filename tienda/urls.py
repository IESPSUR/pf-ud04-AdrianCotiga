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
]
