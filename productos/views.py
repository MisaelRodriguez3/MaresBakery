from django.shortcuts import render, get_object_or_404
from .models import Productos, Opiniones
from django.http import JsonResponse

# Create your views here.


# vistas de las distintas categorias
def mostrar_productos(request):
    productos = Productos.objects.exclude(activo=False)
    return render(request, "categorias/Todos.html", {"productos": productos})


def ver_pan_fino(request):
    pan_fino = Productos.objects.filter(IDcategoria_id=1, activo=True)
    return render(request, "categorias/productos.html", {"productos": pan_fino})


def ver_bolillo_y_pieza(request):
    bolillo_y_pieza = Productos.objects.filter(IDcategoria_id=2, activo=True)
    return render(
        request, "categorias/Bolillo y pieza.html", {"productos": bolillo_y_pieza}
    )


def pan_de_siempre(request):
    mismo = Productos.objects.filter(IDcategoria_id=5, activo=True)
    return render(request, "categorias/El_pan_de_siempre.html", {"productos": mismo})


# Detalle del pan
def detalle_pan(request, producto_id):
    pan = get_object_or_404(Productos, IDproducto=producto_id)
    categoria = pan.IDcategoria
    otros = Productos.objects.filter(IDcategoria_id=categoria).exclude(
        IDproducto=producto_id
    )
    return render(
        request, "descripcion_producto/desc2.html", {"pan": pan, "otros": otros}
    )


# opiniones
def opinion(request, producto_id):
    if request.method == "POST":
        mensaje = request.POST.get("mensaje")
        producto_id = request.POST.get("producto_id")
        opinion = Opiniones(IDproducto_id=producto_id, Opinion=mensaje)
        opinion.save()
    return JsonResponse({})
