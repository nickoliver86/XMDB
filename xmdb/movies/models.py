from django.db import models

# Create your models here.

class Director(models.Model):
    name = models.TextField()

class Writer(models.Model):
    name = models.TextField()

class Actor(models.Model):
    name = models.TextField

class Movie(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    director = models.ForeignKey(Director)
    writer = models.ForeignKey(Writer)
    actors = models.ManyToManyField(Actor)
    #STARRATINGS = [i for i in range(1, 6)]
    #rating = models.IntegerField(max_length=1, choices=STARRATINGS)
    RATED = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, 'R')
    )
    rated = models.IntegerField(choices=RATED)