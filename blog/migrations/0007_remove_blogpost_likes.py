# Generated by Django 4.2.4 on 2023-10-25 00:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogpost_likes_alter_comment_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
    ]