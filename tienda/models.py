from django.db import models

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    unidades = models.IntegerField()
    precio = models.IntegerField()
    detalles = models.TextField(blank=True)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    fecha = models.DateTimeField()
    unidades = models.ForeignKey(Producto, on_delete=models.CASCADE)
    importe = models.IntegerField()

    def __str__(self):
        return str(self.fecha)
