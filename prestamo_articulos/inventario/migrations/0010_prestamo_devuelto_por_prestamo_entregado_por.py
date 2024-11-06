# Generated by Django 5.1.2 on 2024-11-06 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0009_departamento_prestamo_departamento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='devuelto_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestamos_devueltos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='entregado_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prestamos_entregados', to=settings.AUTH_USER_MODEL),
        ),
    ]
