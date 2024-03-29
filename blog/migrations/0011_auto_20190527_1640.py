# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-05-27 13:40
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_blog_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='yayin_taslak',
            field=models.CharField(choices=[('yayin', 'YAYIN'), ('taslak', 'TASLAK')], default='yayin', max_length=6),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, default='default/wall.png', help_text='Kapak fotoğrafı yükleyiniz', null=True, upload_to=blog.models.upload_to, verbose_name='Resim'),
        ),
    ]
