from django.shortcuts import render
from django.views import generic
from tienda.models import Marca

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    marca = Marca.objects.all()
    return render(request, 'tienda/admin/listado.html', { 'marca' : marca })

