# Generated by Django 4.2.3 on 2023-08-01 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0007_encargos_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='encargos',
            name='Total_comision',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facturas',
            name='Total_comision',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
