from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from tienda.models import Producto
from tienda.models import Compra
from tienda.forms import ProductoForm
from tienda.forms import CompraForm
from django.shortcuts import redirect

# Create your views here.
def welcome(request):
    return render(request,'tienda/index.html', {})

def listado(request):
    producto = Producto.objects.all()
    return render(request, 'tienda/admin/listado.html', { 'productos' : producto })

def detalles(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('listado')

    producto_form = ProductoForm(instance=producto)

    return render(request, 'tienda/admin/detalles.html', {'producto_form': producto_form})

def edicion(request):
    producto = Producto.objects.get(id = id)
    formulario = ProductoForm(request.POST or None, request.FILES or None, isinstance=producto)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('listado')
    return render(request, 'tienda/admin/edicion.html', {'formulario': formulario})

def eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    producto.delete()
    return redirect('listado')

def nuevo (request):
    producto = Producto.__new__(Producto)
    producto_form = ProductoForm()

    if request.method == "POST":
        form = ProductoForm(request.POST)

        if form.is_valid():
            producto = form.save(commit=False)
            producto.save()
            return redirect('listado')

    return render(request, 'tienda/admin/detalles.html', {'producto_form': producto_form})

def compra (request):
    producto = Producto.objects.all()
    return render(request, 'tienda/compra.html', { 'productos' : producto })

def checkout (request, pk):
    compra = Compra.__new__(Compra)
    compra_form = CompraForm()

    if request.method == "POST":
        form = CompraForm(request.POST)

    return render(request, 'tienda/checkout.html', {'compra_form': compra_form})
