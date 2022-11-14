from django.shortcuts import render
from django.views import generic
from tienda.models import Producto

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    producto = Producto.objects.all()
    return render(request, 'tienda/admin/listado.html', { 'productos' : producto })

def detalles(request):
    return render(request, 'tienda/admin/detalles.html', {})

def edicion(request):
    return render(request, 'tienda/admin/edicion.html', {})

def eliminar(request):
    return render(request, 'tienda/admin/eliminar.html', {})

def nuevo (request):
    return render(request, 'tienda/admin/nuevo.html', {})
