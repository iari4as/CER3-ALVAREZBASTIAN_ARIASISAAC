# Generated by Django 5.1.2 on 2024-11-24 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_evento_delete_eventoacademico'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(max_length=50)),
                ('estado', models.CharField(choices=[('Pendiente', 'Pendiente'), ('Resuelto', 'Resuelto')], default='Pendiente', max_length=20)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
