# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20150723_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='uzers',
            new_name='users',
        ),
    ]
