# Generated by Django 4.2.1 on 2023-07-22 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0006_remove_categorias_activa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='Precio',
            field=models.FloatField(),
        ),
    ]
