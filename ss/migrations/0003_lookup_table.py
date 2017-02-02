# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-11 19:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ss', '0002_pcr_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='lookup_table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('positive', models.BooleanField(default=False)),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.Species')),
            ],
        ),
    ]
