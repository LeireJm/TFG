from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import check_password as check_password_hasher
from paginaPrincipal.models import Cancion


class Playlist(models.Model):
    playlistId = models.IntegerField()
    playlistName = models.TextField(max_length=200)
    listaCanciones = ArrayField(models.IntegerField(), null=True)

    class Meta:
        db_table = 'playlist'

class UsuarioManager(BaseUserManager):
    def create_user(self, userId, userName, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email debe ser establecido')
        email = self.normalize_email(email)
        user = self.model(userId=userId, userName=userName, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userId, userName, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(userId, userName, email, password, **extra_fields)
    
class Usuario(models.Model):
    userId = models.IntegerField(unique=True)
    userName = models.TextField()
    email = models.TextField(max_length=200, unique=True)
    password = models.TextField(max_length=200)
    favoritos = ArrayField(models.IntegerField(), null=True) #por ahora suponemos que el id de la canción es un número
    playlists = ArrayField(models.IntegerField(), null=True) #playlist contiene el id de cada playlist

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['userId', 'userName']

    @property
    def is_anonymous(self):
        return False  # True si el usuario es anónimo y False si el usuario está autenticado
    
    @property
    def is_authenticated (self):
        return True  # True si el usuario es anónimo y False si el usuario está autenticado
    
    def check_password(self, raw_password):
        return raw_password == self.password
    
    def get_userId(self):
        return self.userId

    class Meta:
        db_table = 'usuarios'
