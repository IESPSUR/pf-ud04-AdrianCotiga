from django.shortcuts import render, get_object_or_404, redirect
from tienda.models import Producto
from tienda.models import Compra
from tienda.models import Marca
from tienda.forms import ProductoForm
from tienda.forms import CompraForm
from django.shortcuts import redirect
from django.db import transaction

def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    producto = Producto.objects.all()
    return render(request, 'tienda/admin/listado.html', { 'productos' : producto })

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
    producto.delete()
    return redirect('listado')

def nuevo (request):
    producto = Producto()
    producto_form = ProductoForm()

    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('listado')

    return render(request, 'tienda/admin/edicion.html', {'producto_form': producto_form})

def compra (request):
    producto = Producto.objects.all()
    return render(request, 'tienda/compra.html', { 'productos' : producto })

@transaction.atomic()
def checkout (request, pk):
    producto = get_object_or_404(Producto, pk=pk);
    compra_form = CompraForm()
    if request.method == "POST":
        form = CompraForm(request.POST)

        if form.is_valid():
            compra = form.save(commit=False)
            compra.producto = producto
            compra.importe = compra.unidades * producto.precio
            producto.unidades = producto.unidades - compra.unidades
            compra.save()
            producto.save()
            return redirect('compra')

    return render(request, 'tienda/checkout.html', {'producto':producto, 'compra_form': compra_form})


def informes (request):
    marca = Marca.objects.all()
    producto = Producto.objects.all()
    compra = Compra.objects.all()
    return render(request, 'tienda/informes.html', {'marcas': marca ,'productos': producto, 'compras': compra})
