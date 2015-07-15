# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_movie_poster'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdbId',
            field=models.TextField(null=True),
        ),
    ]
