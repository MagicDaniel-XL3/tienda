from django.contrib import admin
from .models import Producto, Carrito, Opinion

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock")     # columnas visibles
    search_fields = ("nombre", "descripcion")        # barra de búsqueda
    list_filter = ("precio", "stock")                # filtros laterales
    ordering = ("nombre",)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad")
    search_fields = ("producto__nombre",)
    list_filter = ("cantidad",)


@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "producto", "fecha")
    search_fields = ("nombre", "comentario", "producto__nombre")
    list_filter = ("fecha", "producto")
    ordering = ("-fecha",)
