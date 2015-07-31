# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20150723_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='users',
            new_name='user',
        ),
    ]
