# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-23 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190523_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='slug',
            field=models.SlugField(editable=False, null=True, unique=True),
        ),
    ]
