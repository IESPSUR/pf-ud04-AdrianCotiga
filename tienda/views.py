from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect

from tienda.forms import ProductoForm, CompraForm, FiltroForm, MarcaForm, UsuarioForm
from tienda.models import Producto, Compra


def welcome(request):
    return render(request, 'tienda/index.html', {})


def listado(request):
    producto = Producto.objects.all()

    if request.method == 'GET':
        filtro_nombre = FiltroForm(request.GET)

        if filtro_nombre.is_valid():
            nombre = filtro_nombre.cleaned_data['nombre']

            if nombre:
                producto = Producto.objects.filter(nombre__icontains=nombre)

    return render(request, 'tienda/admin/listado.html', {'productos': producto, 'filtro_form': filtro_nombre})


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

    return render(request, 'tienda/admin/eliminar.html', {'productos': producto})


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

    if request.method == 'POST':
        compra_form = CompraForm(request.POST)

        if compra_form.is_valid():
            compra = compra_form.save(commit=False)
            compra.producto = producto
            compra.importe = compra.unidades * producto.precio
            compra.usuario = request.user

            if compra.unidades > producto.unidades:
                errorInsuficientesUnidades = "No hay suficientes unidades disponibles de "
                return render(request, 'tienda/compra.html',
                              {'productos': producto, 'compra_form': compra_form,
                               'errorInsuficientesUnidades': errorInsuficientesUnidades})

            producto.unidades -= compra.unidades
            producto.save()
            compra.save()
            return redirect('compra')

    else:
        compra_form = CompraForm()

    return render(request, 'tienda/compra.html', {'productos': producto, 'compra_form': compra_form})


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

            if compra.unidades > producto.unidades:
                errorInsuficientesUnidades = "No hay suficientes unidades disponibles de "
                return render(request, 'tienda/checkout.html',
                              {'productos': producto, 'compra_form': compra_form,
                               'errorInsuficientesUnidades': errorInsuficientesUnidades})

            producto.unidades -= compra.unidades
            producto.save()
            compra.save()
            return redirect('compra')

    else:
        compra_form = CompraForm()

    return render(request, 'tienda/checkout.html', {'productos': producto, 'compra_form': compra_form})


def informes(request):
    return render(request, 'tienda/informes.html', {})


def productosMarca(request):
    if request.GET.get("marca"):
        filtro_marca = MarcaForm(request.GET)

        if filtro_marca.is_valid():
            marca = filtro_marca.cleaned_data.get('marca')
            productos = Producto.objects.filter(marca__nombre=marca)

    else:
        filtro_marca = MarcaForm()
        productos = Producto.objects.all()

    return render(request, 'tienda/informes/productosMarca.html',
                  {'productos': productos, 'filtro_marca': filtro_marca})


def productosVendidos(request):
    productos_vendidos = Producto.objects.annotate(total_vendido=Sum('compra__unidades')).order_by('-total_vendido')[
                         :10]

    return render(request, 'tienda/informes/productosVendidos.html', {'productos_vendidos': productos_vendidos})


def comprasUsuario(request):
    if request.GET.get("usuario"):
        filtro_usuario = UsuarioForm(request.GET)

        if filtro_usuario.is_valid():
            usuario = filtro_usuario.cleaned_data.get('usuario')
            compras = Compra.objects.filter(usuario__username=usuario.username)

    else:
        filtro_usuario = UsuarioForm()
        compras = Compra.objects.all()

    return render(request, 'tienda/informes/comprasUsuario.html',
                  {'compras': compras, 'filtro_usuario': filtro_usuario})


def mejoresClientes(request):
    mejores_clientes = User.objects.annotate(total_gastado=Sum('compra__importe')).order_by('-total_gastado')[:10]

    return render(request, 'tienda/informes/mejoresClientes.html', {'mejores_clientes': mejores_clientes})
