from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),  # Página principal
    path('tienda/', views.tienda, name='tienda'),
    path('contacto/', views.contacto, name='contacto'),
    path('formulario/', views.formulario, name='formulario'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),

    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/actualizar/<int:producto_id>/<str:accion>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
     path('carrito/finalizar/', views.finalizar_compra, name='finalizar_compra'),
]
