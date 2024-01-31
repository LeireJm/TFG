from django.db import models

# Create your models here.

class Cancion(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    top_genre = models.CharField(max_length=200)
    year = models.IntegerField()
    bpm = models.IntegerField()
    nrgy = models.IntegerField()
    dnce = models.IntegerField()
    dB = models.IntegerField()
    live = models.IntegerField()
    val = models.IntegerField()
    dur = models.IntegerField()
    acous = models.IntegerField()
    spch = models.IntegerField()
    pop = models.IntegerField()

    class Meta:
        db_table = 'cancion'


class Rating(models.Model):
    userId = models.IntegerField()
    songId = models.IntegerField()
    rating = models.IntegerField()
    timestamp = models.BigIntegerField()

    class Meta:
        db_table = 'rating'