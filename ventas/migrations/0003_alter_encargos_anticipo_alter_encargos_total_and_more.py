# Generated by Django 4.2.1 on 2023-07-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_remove_encargos_recibio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encargos',
            name='Anticipo',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='encargos',
            name='Total',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='facturas',
            name='Total_a_pagar',
            field=models.FloatField(),
        ),
    ]
