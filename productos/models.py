from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='productos/')
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre


class Carrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"


class Opinion(models.Model):
    producto = models.ForeignKey(Producto, related_name="opiniones", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # nombre del visitante
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Opinión"
        verbose_name_plural = "Opiniones"
        
    def __str__(self):
        return f"{self.nombre} - {self.producto.nombre}"
