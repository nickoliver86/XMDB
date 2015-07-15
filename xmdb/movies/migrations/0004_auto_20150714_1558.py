# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_movie_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='actors',
            field=models.ManyToManyField(blank=True, null=True, to='movies.Actor'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(null=True, blank=True, to='movies.Director'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='rated',
            field=models.IntegerField(choices=[(1, 'G'), (2, 'PG'), (3, 'PG-13'), (4, 'R')], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='movie_thumbnails', null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='writer',
            field=models.ForeignKey(null=True, blank=True, to='movies.Writer'),
        ),
    ]
