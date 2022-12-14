from django import forms
from .models import Producto
from .models import Compra

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['unidades']
        unidades = forms.IntegerField(min_value=1)
