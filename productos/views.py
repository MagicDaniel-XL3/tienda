from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, Opinion
from django.contrib import messages
from .forms import OpinionForm

# Vistas básicas
def encabezado(request):
    return render(request, "productos/encabezado.html")

def contacto(request):
    return render(request, "productos/contacto.html")

def formulario(request):
    return render(request, "productos/formulario.html")

# Tienda de productos
def tienda(request):
    productos = Producto.objects.all()
    return render(request, "productos/tienda.html", {"productos": productos})

def principal(request):
    productos = Producto.objects.all()
    return render(request, "productos/principal.html", {"productos": productos})

# Agregar producto al carrito
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    carrito = request.session.get('carrito', {})

    if str(producto.id) in carrito:
        # Si ya está en el carrito, no permitir exceder stock
        if carrito[str(producto.id)]["cantidad"] < producto.stock:
            carrito[str(producto.id)]["cantidad"] += 1
    else:
        if producto.stock > 0:  # Solo agregar si hay stock
            carrito[str(producto.id)] = {
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": 1,
            }
        else:
            # Opcional: mensaje de alerta si no hay stock
            # messages.warning(request, "No hay stock disponible")
            pass

    request.session["carrito"] = carrito
    return redirect("ver_carrito")


# Ver carrito
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = 0

    for id, item in carrito.items():
        item['subtotal'] = item['precio'] * item['cantidad']
        total += item['subtotal']

    return render(request, "productos/carrito.html", {"carrito": carrito, "total": total})


# Vaciar carrito (opcional)
def vaciar_carrito(request):
    request.session["carrito"] = {}
    return redirect("ver_carrito")

# Actualizar cantidad de un producto
def actualizar_carrito(request, producto_id, accion):
    carrito = request.session.get('carrito', {})
    producto = get_object_or_404(Producto, id=producto_id)

    producto_id = str(producto_id)
    if producto_id in carrito:
        if accion == 'sumar':
            if carrito[producto_id]['cantidad'] < producto.stock:
                carrito[producto_id]['cantidad'] += 1
        elif accion == 'restar':
            carrito[producto_id]['cantidad'] -= 1
            if carrito[producto_id]['cantidad'] <= 0:
                del carrito[producto_id]

    request.session['carrito'] = carrito
    return redirect('ver_carrito')

from django.contrib import messages

def finalizar_compra(request):
    # Vaciar el carrito
    request.session['carrito'] = {}
    # Mensaje de éxito
    messages.success(request, "¡Tu compra ha sido realizada con éxito!")
    return redirect('principal')  # Redirige al inicio

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    opiniones = producto.opiniones.all().order_by("-fecha")

    if request.method == "POST":
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.producto = producto
            opinion.save()
            return redirect("detalle_producto", producto_id=producto.id)
    else:
        form = OpinionForm()

    return render(request, "productos/detalle.html", {
        "producto": producto,
        "opiniones": opiniones,
        "form": form
    })
