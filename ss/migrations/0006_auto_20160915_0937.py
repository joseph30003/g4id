# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-15 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ss', '0005_lookup_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCR_data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='PCR_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ward_1', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('ward_2', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('age', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('PCR', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('PCR_result', models.CharField(blank=True, default=None, max_length=10, null=True)),
                ('RPPCR_date', models.IntegerField()),
                ('sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.Sample')),
            ],
        ),
        migrations.CreateModel(
            name='PCR_target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='pcr_result',
            name='sample',
        ),
        migrations.AlterField(
            model_name='lookup_table',
            name='positive',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.PCR_target'),
        ),
        migrations.DeleteModel(
            name='PCR_result',
        ),
        migrations.AddField(
            model_name='pcr_data',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ss.PCR_target'),
        ),
    ]
