# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-08-07 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0002_job'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('start', models.IntegerField(max_length=45)),
                ('end', models.IntegerField(max_length=45)),
                ('plan', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='exam_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='job',
            name='creator',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
    ]
