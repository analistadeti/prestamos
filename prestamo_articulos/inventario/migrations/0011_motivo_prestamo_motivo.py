# Generated by Django 5.1.2 on 2024-11-06 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_prestamo_devuelto_por_prestamo_entregado_por'),
    ]

    operations = [
        migrations.CreateModel(
            name='Motivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='prestamo',
            name='motivo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.motivo'),
        ),
    ]
