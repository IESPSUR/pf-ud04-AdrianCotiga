from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"

class CompraForm(forms.Form):
    unidades = forms.IntegerField(min_value=1)
