from django.db.models import Q
from django.shortcuts import render
from productos.models import Categorias, Productos

# Create your views here.


def home(request):
    trending_productos = Productos.objects.filter(IDcategoria_id=5)
    return render(
        request, "inicio/home.html", {"trending_productos": trending_productos}
    )


def buscar_productos(request):
    busqueda = request.GET.get("cuadro")
    productos = Productos.objects.filter(Q(Nombre__icontains=busqueda))
    resultados = {
        "productos": [
            {
                "ID": producto.IDproducto,
                "Nombre": producto.Nombre,
                "Precio": producto.Precio,
                "Imagen": producto.Imagen,
            } 
            for producto in productos
        ]
    }
    return render(request, "inicio/busqueda.html", {"resultados": resultados})
