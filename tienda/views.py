from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from tienda.forms import ProductoForm, CompraForm
from tienda.models import Producto


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    if request.method == 'GET':
        nombre = request.POST.get('nombre')
        producto = Producto.objects.filter(nombre__icontains=nombre) #crear un formulario en forms.py

    else:
        producto = Producto.objects.all()

    return render(request, 'tienda/admin/listado.html', {'producto': producto})


def edicion(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            producto.save()
            return redirect('listado')

    producto_form = ProductoForm(instance=producto)

    return render(request, 'tienda/admin/edicion.html', {'producto_form': producto_form})


def eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        return redirect('listado')

    return render(request, 'tienda/admin/eliminar.html', {'producto': producto})


def nuevo(request):
    producto_form = ProductoForm()

    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('listado')

    return render(request, 'tienda/admin/edicion.html', {'producto_form': producto_form})


def compra(request):
    producto = Producto.objects.all()
    return render(request, 'tienda/compra.html', {'producto': producto})

@transaction.atomic()
def checkout(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)

        if compra_form.is_valid():
            compra = compra_form.save(commit=False)
            compra.producto = producto
            compra.importe = compra.unidades * producto.precio
            compra.usuario = request.user
            producto.unidades -= compra.unidades
            producto.save()
            compra.save()
            return redirect('compra')

    else:
        compra_form = CompraForm()

    return render(request, 'tienda/checkout.html', {'producto': producto, 'compra_form': compra_form})