import itertools

from django import forms
from django.contrib.auth.models import User

from .models import Producto, Compra, Marca


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'modelo', 'marca', 'unidades', 'precio', 'detalles']


class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['unidades']


class CheckoutForm(forms.ModelForm):
    unidades = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Compra
        fields = ['unidades']


class FiltroForm(forms.ModelForm):
    nombre = forms.CharField(required=False)

    class Meta:
        model = Producto
        fields = ['nombre']


class MarcaForm(forms.Form):
    choices = Marca.objects.all().values_list('nombre', 'nombre')
    empty = [('', '--------')]
    marca = forms.ChoiceField(required=False, choices=itertools.chain(empty, choices.iterator()))


class UsuarioForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
