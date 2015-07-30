from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Director(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Writer(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name

# class User(User):
#     def __str__(self):
#         return self.username

class Movie(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    director = models.ForeignKey(Director, null=True, blank=True)
    writer = models.ForeignKey(Writer, null=True, blank=True)
    actors = models.ManyToManyField(Actor, blank=True)
    RATED = (
        (1, 'G'),
        (2, 'PG'),
        (3, 'PG-13'),
        (4, 'R')
    )
    rated = models.IntegerField(choices=RATED, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="movie_thumbnails", null=True, blank=True)
    poster = models.TextField(null=True)
    imdbId = models.TextField(null=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return "%s (%d)" % (self.name, int(self.year))


