# Generated by Django 5.0.6 on 2024-11-01 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_articulo_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='codigo',
        ),
        migrations.AlterField(
            model_name='articulo',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
