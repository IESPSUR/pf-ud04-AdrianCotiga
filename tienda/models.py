from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.utils import timezone


class Marca(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True, unique=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    unidades = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    detalles = models.TextField(blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    producto = models.ForeignKey(Producto, models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    importe = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.00)])
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.fecha, self.usuario, self.producto)
