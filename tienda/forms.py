from django import forms
from .models import Producto, Compra


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__" #poner todos los campos

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['unidades']
        unidades = forms.IntegerField(min_value=1)

class FiltroForm(forms.ModelForm):
    nombre = forms.CharField(required=False)

    class Meta:
        model = Producto
        fields = ['nombre']
