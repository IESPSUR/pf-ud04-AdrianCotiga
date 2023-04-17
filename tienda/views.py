from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from tienda.forms import ProductoForm, CompraForm, FiltroForm, MarcaForm, UsuarioForm, CheckoutForm
from tienda.models import Producto, Compra
from django.core.exceptions import ValidationError


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

                if not producto:
                    messages.warning(request, "Ningún producto existente con el nombre " + nombre + ".")

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


def nuevo(request):
    producto_form = ProductoForm()

    if request.method == "POST":
        producto_form = ProductoForm(request.POST)

        if producto_form.is_valid():
            producto = producto_form.save(commit=False)
            producto.save()
            return redirect('listado')

    return render(request, 'tienda/admin/edicion.html', {'producto_form': producto_form})


def eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == "POST":
        producto.delete()
        return redirect('listado')

    return render(request, 'tienda/admin/eliminar.html', {'productos': producto})


def compra(request):
    producto = Producto.objects.all()
    compra_form = CompraForm()

    return render(request, 'tienda/compra.html', {'productos': producto, 'compra_form': compra_form})


@transaction.atomic()
def checkout(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    compra_unidades = int(request.GET.get('unidades'))
    importe = 0

    if request.method == 'GET':
        precio_total = producto.precio * compra_unidades

        if compra_unidades <= 0:
            messages.warning(request, "Introduzca un número mayor o igual a 1.")
            return redirect('compra')

        if compra_unidades > producto.unidades:
            messages.warning(request, "Se están intentando comprar más unidades de las disponibles.")
            return redirect('compra')

    elif request.method == 'POST':
        importe = compra_unidades * producto.precio
        compra = Compra(producto=producto, unidades=compra_unidades, importe=importe)
        compra.usuario = request.user
        compra.save()
        producto.unidades -= compra_unidades
        producto.save()
        messages.success(request, "Artículo: " + producto.nombre + " comprado con éxito.")
        return redirect('compra')

    return render(request, 'tienda/checkout.html',
                  {'producto': producto, 'precio_total': precio_total, 'compra_unidades': compra_unidades,
                   'importe': importe})


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
