# Generated by Django 5.0.2 on 2024-03-03 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cancion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('songId', models.IntegerField()),
                ('artist_name', models.CharField(max_length=200)),
                ('track_name', models.CharField(max_length=200)),
                ('track_id', models.CharField(max_length=200)),
                ('popularity', models.IntegerField(null=True)),
                ('year', models.IntegerField(null=True)),
                ('genre', models.IntegerField(null=True)),
                ('danceability', models.IntegerField(null=True)),
                ('energy', models.IntegerField(null=True)),
                ('key', models.IntegerField(null=True)),
                ('loudness', models.IntegerField(null=True)),
                ('mode', models.IntegerField(null=True)),
                ('acousticness', models.IntegerField(null=True)),
                ('instrumentalness', models.IntegerField(null=True)),
                ('liveness', models.IntegerField(null=True)),
                ('valence', models.IntegerField(null=True)),
                ('tempo', models.IntegerField(null=True)),
                ('duration_ms', models.IntegerField(null=True)),
                ('time_signature', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'cancion',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userId', models.IntegerField()),
                ('songId', models.IntegerField()),
                ('rating', models.IntegerField()),
                ('timestamp', models.BigIntegerField()),
            ],
            options={
                'db_table': 'rating',
            },
        ),
    ]
