# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-11 15:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_mediaitem_resource_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mediaitem',
            old_name='postive',
            new_name='positive',
        ),
    ]
