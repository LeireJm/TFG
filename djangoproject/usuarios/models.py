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
    email = models.TextField(max_length=200, unique=True)
    password = models.TextField(max_length=200)
    favoritos = ArrayField(models.IntegerField(), null=True) #por ahora suponemos que el id de la canción es un número
    playlists = models.ManyToManyField(Playlist) #playlist contiene el id de cada playlist

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userId', 'userName']

    @property
    def is_anonymous(self):
        return False  # True si el usuario es anónimo y False si el usuario está autenticado
    
    @property
    def is_authenticated (self):
        return True  # True si el usuario es anónimo y False si el usuario está autenticado

    class Meta:
        db_table = 'usuarios'
