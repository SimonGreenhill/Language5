# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 20:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0002_task_source_can_be_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lexicon',
            field=models.ManyToManyField(blank=True, help_text=b'Saved Lexical Items', to='lexicon.Lexicon'),
        ),
    ]
