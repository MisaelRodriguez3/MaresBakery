from django.contrib import admin
from .models import Productos, Categorias, Opiniones

# Register your models here.
def activar(modeladmin, request, queryset):
    queryset.update(activo=True)

def desactivar(modeladmin, request, queryset):
    queryset.update(activo=False)

class CategoriasAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_categoria')
    ordering = ('IDcategoria',)
    search_fields = ('Nombre_categoria',)

class ProductosAdmin(admin.ModelAdmin):
    list_display = ('id', 'Nombre', 'descripcion', 'precio', 'categoria', 'img', 'activo')
    ordering = ('IDproducto',)
    search_fields = ('Nombre',)
    list_filter = ('IDcategoria__Nombre_categoria',)
    actions = [activar, desactivar]

class OpinionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'opinion')
    search_fields = ('IDproducto__Nombre',)
    ordering = ('IDopinion')
    
admin.site.register(Productos, ProductosAdmin)
admin.site.register(Categorias, CategoriasAdmin)
admin.site.register(Opiniones, OpinionesAdmin)
