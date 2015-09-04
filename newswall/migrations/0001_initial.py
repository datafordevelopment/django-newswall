# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('priority', models.SmallIntegerField(default=0, help_text='Set the priority in case of cross posts. Higher is better.', verbose_name='priority')),
                ('show_min', models.PositiveSmallIntegerField(default=0, help_text='Show at least this many entries', verbose_name='Show at least')),
                ('source', models.CharField(blank=True, max_length=10, verbose_name='source', choices=[(b'facebook', 'Facebook'), (b'twitter', 'Twitter'), (b'blog', 'Elephantblog'), (b'rss', 'RSS')])),
                ('data', models.TextField(verbose_name='configuration data', blank=True)),
            ],
            options={
                'ordering': ['priority', 'name'],
                'verbose_name': 'source',
                'verbose_name_plural': 'sources',
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp')),
                ('object_url', models.URLField(unique=True, verbose_name='object URL')),
                ('title', models.CharField(max_length=1000, verbose_name='title')),
                ('author', models.CharField(max_length=100, verbose_name='author', blank=True)),
                ('body', models.TextField(help_text='Content of the story. May contain HTML.', verbose_name='body', blank=True)),
                ('image_url', models.CharField(max_length=1000, verbose_name='image URL', blank=True)),
                ('source', models.ForeignKey(related_name='stories', verbose_name='source', to='newswall.Source')),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': 'story',
                'verbose_name_plural': 'stories',
            },
        ),
    ]
