# Generated by Django 5.0.3 on 2024-11-02 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_remove_articulo_prestado'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='entregado',
            field=models.BooleanField(default=False),
        ),
    ]
