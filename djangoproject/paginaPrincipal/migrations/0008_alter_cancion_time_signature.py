# Generated by Django 5.0.2 on 2024-03-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paginaPrincipal', '0007_alter_cancion_acousticness_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cancion',
            name='time_signature',
            field=models.DecimalField(decimal_places=5, max_digits=20, null=True),
        ),
    ]
