# Generated by Django 5.0.2 on 2024-03-02 12:47

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0004_alter_usuario_email_alter_usuario_userid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='listaCanciones',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='playlists',
        ),
        migrations.AddField(
            model_name='playlist',
            name='listaCanciones',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
        migrations.AddField(
            model_name='usuario',
            name='playlists',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None),
        ),
    ]
