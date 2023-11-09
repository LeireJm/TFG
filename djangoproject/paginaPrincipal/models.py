from django.db import models

# Create your models here.
#creo una nueva tabla en la bd

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