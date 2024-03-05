from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Cancion(models.Model):
    artist_name = models.CharField(max_length=200)
    track_name = models.CharField(max_length=200)
    track_id = models.CharField(max_length=200)
    popularity = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    genre = models.CharField(max_length=200, null=True)
    danceability = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    energy = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    key = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    loudness = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    mode = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    speechiness = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    acousticness = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    instrumentalness = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    liveness = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    valence = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    tempo = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    duration_ms = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    time_signature = models.DecimalField(null=True, max_digits=50, decimal_places=6)
    genres = ArrayField(models.CharField(), null=True)

    class Meta:
        db_table = 'cancion'


class Rating(models.Model):
    userId = models.IntegerField()
    songId = models.IntegerField()
    rating = models.IntegerField()
    timestamp = models.BigIntegerField()

    class Meta:
        db_table = 'rating'