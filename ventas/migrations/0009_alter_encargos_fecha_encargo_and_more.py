# Generated by Django 4.2.1 on 2023-08-02 01:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0008_encargos_total_comision_facturas_total_comision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encargos',
            name='Fecha_encargo',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='Fecha_pedido',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
