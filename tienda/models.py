from django.db import models
from django.conf import settings
from django.utils import timezone


class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    unidades = models.IntegerField() #falta valor min y max
    precio = models.IntegerField() #el precio puede tener decimales
    detalles = models.TextField(blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    producto = models.ForeignKey(Producto, models.PROTECT)
    fecha = models.DateTimeField(default=timezone.now)
    unidades = models.PositiveIntegerField()
    importe = models.IntegerField()
    comprador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha)
