# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-27 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20190526_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='default/wall.png', help_text='Kapak fotoğrafı yükleyiniz', null=True, upload_to='', verbose_name='Resim'),
        ),
    ]
