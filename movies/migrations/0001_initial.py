# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('year', models.IntegerField()),
                ('rated', models.IntegerField(choices=[(1, 'G'), (2, 'PG'), (3, 'PG-13'), (4, 'R')], blank=True, null=True)),
                ('thumbnail', models.ImageField(blank=True, upload_to='movie_thumbnails', null=True)),
                ('poster', models.TextField(null=True)),
                ('imdbId', models.TextField(null=True)),
                ('actors', models.ManyToManyField(blank=True, to='movies.Actor')),
                ('director', models.ForeignKey(null=True, blank=True, to='movies.Director')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Writer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='writer',
            field=models.ForeignKey(null=True, blank=True, to='movies.Writer'),
        ),
    ]
