from django.db import models
from django.contrib.postgres.fields import ArrayField
from paginaPrincipal.models import Cancion

class Playlist(models.Model):
    playlistId = models.IntegerField()
    playlistName = models.TextField(max_length=200)
    listaCanciones = models.ManyToManyField(Cancion)

    class Meta:
        db_table = 'playlist'

class Usuario(models.Model):
    userId = models.IntegerField()
    userName = models.TextField()
    email = models.TextField(max_length=200)
    password = models.TextField(max_length=200)
    favoritos = ArrayField(models.IntegerField(), null=True) #por ahora suponemos que el id de la canción es un número
    playlists = models.ManyToManyField(Playlist) #playlist contiene el id de cada playlist

    class Meta:
        db_table = 'usuarios'
