from django.shortcuts import render, get_object_or_404, redirect

from tienda.forms import ProductoForm
from tienda.models import Producto


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
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
