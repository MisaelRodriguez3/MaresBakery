# Generated by Django 4.2.1 on 2023-07-22 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0007_alter_productos_precio'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='categorias',
            table='Categorias',
        ),
        migrations.AlterModelTable(
            name='opiniones',
            table='Opiniones',
        ),
        migrations.AlterModelTable(
            name='productos',
            table='Productos',
        ),
    ]
