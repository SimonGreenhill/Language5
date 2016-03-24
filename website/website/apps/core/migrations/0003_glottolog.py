# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_fix_classification'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='glottocode',
            field=models.CharField(blank=True, db_index=True, help_text=b'Glottolog Code.', max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='details',
            field=models.CharField(blank=True, help_text=b'Extra details e.g. page number', max_length=32, null=True),
        ),
    ]