from django.contrib import admin
from .models import Facturas, Encargos, Info_encargos, Info_facturas, Clientes_encargos, Clientes_facturas 
# Register your models here.

class FacturasAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'total_pp', 'transaccion', 'fecha',)
    ordering = ('IDfactura',)
    search_fields = ('IDfactura', 'cliente',)
    list_filter = ('Fecha_pedido',)

class EncargosAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'Anticipo', 'total_pp', 'transaccion', 'fechaa', 'fechab',)
    ordering = ('IDencargo',)
    search_fields = ('IDencargo', 'cliente',)
    list_filter = ('Fecha_encargo', 'Fecha_entrega',)


class Info_facturasAdmin(admin.ModelAdmin):
    list_display = ('id', 'idcompra', 'producto', 'cantidad',)
    ordering =('IDinfo_factura',)
    list_filter = ('IDinfo_factura',)

class Info_encargosAdmin(admin.ModelAdmin):
    list_display = ('id', 'idencargo', 'producto', 'Cantidad',)
    ordering = ('IDinfo_encargos',)
    list_filter = ('IDinfo_encargo',)

class Clientes_facturasAdmin(admin.ModelAdmin):
    list_display = ('ID', 'cliente', 'compra',)
    ordering = ('ID',)
    search_fields = ('IDcliente__username',)

class Clientes_encargosAdmin(admin.ModelAdmin):
    list_display = ('ID', 'cliente', 'encargo',)
    ordering = ('ID',)
    search_fields = ('IDcliente__username',)



admin.site.register(Facturas, FacturasAdmin)
admin.site.register(Encargos, EncargosAdmin)
admin.site.register(Info_encargos, Info_encargosAdmin)
admin.site.register(Info_facturas, Info_facturasAdmin)
admin.site.register(Clientes_encargos, Clientes_encargosAdmin)
admin.site.register(Clientes_facturas, Clientes_facturasAdmin)