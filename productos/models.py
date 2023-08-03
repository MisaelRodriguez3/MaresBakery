from django.db import models

# Create your models here.
class Categorias(models.Model):
    IDcategoria = models.AutoField(primary_key=True)
    Nombre_categoria = models.CharField(max_length=255)

    def id(self):
        return self.IDcategoria
    
    def nombre_categoria(self):
        return self.Nombre_categoria
    
    id.short_description = 'ID Categoría'
    nombre_categoria.short_description = 'Nombre de la Categoría'

    class Meta:
        db_table = 'Categorias'

    def __str__(self):
        return self.Nombre_categoria

class Productos(models.Model):
    IDproducto = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=255)
    Descripcion = models.TextField()
    Precio = models.FloatField()
    IDcategoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    Imagen = models.URLField()
    activo = models.BooleanField(default=True)

    def id(self):
        return self.IDproducto
    
    def precio(self):
        return f"$ {self.Precio}"
    
    def descripcion(self):
        return self.Descripcion
    
    def img(self):
        return self.Imagen
    
    def categoria(self):
        return self.IDcategoria.Nombre_categoria
    
    id.short_description = 'ID Producto'
    precio.short_description = 'Precio'
    categoria.short_description = 'Categoría'
    descripcion.short_description = 'Descripción'
    img.short_description = 'URL de la Imagen'

    class Meta:
        db_table = 'Productos'

    def __str__(self):
        return f'{self.Nombre} -> {self.Precio}'

class Opiniones(models.Model):
    IDopinion = models.AutoField(primary_key=True)
    IDproducto = models.ForeignKey(Productos, on_delete=models.CASCADE)
    Opinion = models.CharField(max_length=255)

    def id(self):
        return self.Opinion
    
    def producto(self):
        return self.IDproducto.Nombre
    
    def opinion(self):
        return self.Opinion

    id.short_description = 'ID Opinión'
    producto.short_description = 'Producto'
    opinion.short_description = 'Opinión'

    class Meta:
        db_table = 'Opiniones'