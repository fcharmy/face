# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 11:40
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=10240)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('create_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[\\w\\s.@+-]+$')])),
                ('description', models.CharField(default='', max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$')])),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=30)),
                ('note', models.CharField(blank=True, max_length=200)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Person_To_Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_tech.Group')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_tech.Person')),
            ],
        ),
        migrations.AddField(
            model_name='face',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='face_tech.Person'),
        ),
    ]
