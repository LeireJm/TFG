# Generated by Django 5.0.2 on 2024-02-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_usuario_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.TextField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='userId',
            field=models.IntegerField(unique=True),
        ),
    ]