# Generated by Django 5.0.6 on 2024-11-01 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0002_prestamo'),
    ]

    operations = [
        migrations.AddField(
            model_name='articulo',
            name='codigo',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]