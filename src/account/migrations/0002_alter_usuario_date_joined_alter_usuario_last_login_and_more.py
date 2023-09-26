# Generated by Django 4.2.4 on 2023-09-23 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(auto_now=True, verbose_name='Ultimo inicio de sesión'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(max_length=30, unique=True, verbose_name='Nombre de usuario'),
        ),
    ]