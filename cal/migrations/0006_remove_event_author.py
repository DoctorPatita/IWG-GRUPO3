# Generated by Django 4.2.5 on 2023-11-16 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cal', '0005_alter_event_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='author',
        ),
    ]