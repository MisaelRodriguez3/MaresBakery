from django.db import models
from django.contrib.auth.models import User
from productos.models import Productos
from django.utils import timezone

# Create your models here.
class Encargos(models.Model):
    IDencargo = models.AutoField(primary_key=True)
    Fecha_encargo = models.DateTimeField(default=timezone.now)
    Fecha_entrega = models.DateField()
    IDcliente = models.ForeignKey(User, on_delete=models.CASCADE)
    Anticipo = models.FloatField()
    Total = models.FloatField()
    Total_comision = models.FloatField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    def id(self):
        return self.IDencargo
    
    def fechaa(self):
        return self.Fecha_encargo
    
    def fechab(self):
        return self.Fecha_entrega
    
    def cliente(self):
        return self.IDcliente.username
    
    def total(self):
        return f"$ {self.Total}"

    def total_pp(self):
        return f"$ {self.Total_comision}"
    
    def transaccion(self):
        return self.transaction_id
    
    id.short_description = 'ID del Encargo'
    fechaa.short_description = 'Fecha del encargo'
    fechab.short_description = 'Fecha de entrega'
    cliente.short_description = 'Cliente'
    total.short_description = 'Total'
    total_pp.short_description = 'Total con comisión'
    transaccion.short_description = 'ID de la Transacción'

    class Meta:
        db_table = 'Encargos'

    def __str__(self):
        return self.IDencargo

class Facturas(models.Model):
    IDfactura = models.AutoField(primary_key=True)
    Fecha_pedido = models.DateTimeField(default=timezone.now)
    IDcliente = models.ForeignKey(User, on_delete=models.CASCADE)
    Total_a_pagar = models.FloatField()
    Total_comision = models.FloatField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True)

    def id(self):
        return self.IDfactura
    
    def fecha(self):
        return self.Fecha_pedido
    
    def cliente(self):
        return self.IDcliente.username
    
    def total(self):
        return f"$ {self.Total_a_pagar}"
    
    def total_pp(self):
        return f" ${self.Total_comision}"
    
    def transaccion(self):
        return self.transaction_id
    
    id.short_description = 'ID de la Compra'
    fecha.short_description = 'Fecha de Compra'
    cliente.short_description = 'Cliente'
    total.short_description = 'Total'
    total_pp.short_description = 'Total con comisión'
    transaccion.short_description = 'ID de la Transacción'

    class Meta:
        db_table = 'Facturas'

    def __str__(self):
        return self.IDfactura

class Info_facturas(models.Model):
    IDinfo_factura = models.AutoField(primary_key=True)
    IDfactura = models.ForeignKey(Facturas, on_delete=models.CASCADE)
    IDproducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def id(self):
        return self.IDinfo_factura
    
    def idcompra(self):
        return self.IDfactura
    
    def producto(self):
        return self.IDproducto.Nombre
    
    id.short_description = 'ID'
    idcompra.short_description = 'ID de la Compra'
    producto.short_description = 'Productos'

    class Meta:
        db_table = 'Info_facturas'

class Clientes_encargos(models.Model):
    ID = models.AutoField(primary_key=True)
    IDcliente = models.ForeignKey(User, on_delete=models.CASCADE)
    IDencargo = models.ForeignKey(Encargos, on_delete=models.CASCADE)

    def cliente(self):
        return self.IDcliente.username
    
    def encargo(self):
        return self.IDencargo
    
    cliente.short_description = 'Cliente'
    encargo.short_description = 'ID del encargo'

    class Meta:
        db_table = 'Clientes_encargos'

class Clientes_facturas(models.Model):
    ID = models.AutoField(primary_key=True)
    IDcliente = models.ForeignKey(User, on_delete=models.CASCADE)
    IDfactura = models.ForeignKey(Facturas, on_delete=models.CASCADE)

    def cliente(self):
        return self.IDcliente.username
    
    def compra(self):
        return self.IDfactura
    
    cliente.short_description = 'Cliente'
    compra.short_description = 'ID de la Compra'

    class Meta:
        db_table = 'Clientes_facturas'

class Info_encargos(models.Model):
    IDinfo_encargos = models.AutoField(primary_key=True)
    IDencargo = models.ForeignKey(Encargos, on_delete=models.CASCADE)
    IDproducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Cantidad = models.IntegerField()

    def id(self):
        return self.IDinfo_encargos
    
    def idencargo(self):
        return self.IDencargo.IDencargo
    
    def producto(self):
        return self.IDproducto.Nombre
    
    id.short_description = 'ID'
    idencargo.short_description = 'ID del Encargo'
    producto.short_description = 'Productos'

    class Meta:
        db_table = 'Info_encargos'