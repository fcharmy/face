# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-23 06:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attend_server', '0003_auto_20170723_0643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor_students',
            name='student',
        ),
        migrations.RemoveField(
            model_name='tutor_students',
            name='tutor',
        ),
        migrations.DeleteModel(
            name='Tutor_Students',
        ),
    ]