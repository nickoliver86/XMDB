# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='thumbnail',
            field=models.ImageField(blank=True, upload_to='', null=True),
        ),
    ]
