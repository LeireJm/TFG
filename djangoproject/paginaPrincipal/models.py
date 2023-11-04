from django.db import models

# Create your models here.
#creo una nueva tabla en la bd

class Cancion(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    top_genre = models.CharField(max_length=200)
    year = models.IntegerField(default=0)
    dur = models.IntegerField(default=0)
    pop = models.IntegerField(default=0)

    class Meta:
        db_table = 'cancion'