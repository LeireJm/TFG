# Generated by Django 5.0.2 on 2024-03-07 16:27

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField(unique=True)),
                ('userName', models.TextField()),
                ('email', models.TextField(max_length=200, unique=True)),
                ('password', models.TextField(max_length=200)),
                ('favoritos', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
                ('playlists', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
            ],
            options={
                'db_table': 'usuarios',
            },
        ),
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playlistId', models.IntegerField()),
                ('playlistName', models.TextField(max_length=200)),
                ('listaCanciones', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=None)),
            ],
            options={
                'db_table': 'playlist',
            },
        ),
    ]
