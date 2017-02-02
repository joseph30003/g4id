# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-09 19:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ss', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCR_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_1', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('ward_2', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('age', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('PCR', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('PCR_result', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('RPPCR_date', models.IntegerField()),
                ('positive_1', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('positive_2', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('positive_3', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('positive_4', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.Sample')),
            ],
        ),
    ]
