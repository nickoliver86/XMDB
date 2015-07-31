# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20150723_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='thumbnail',
        ),
    ]
