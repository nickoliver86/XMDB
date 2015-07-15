# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20150715_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='poster',
            field=models.TextField(null=True),
        ),
    ]
