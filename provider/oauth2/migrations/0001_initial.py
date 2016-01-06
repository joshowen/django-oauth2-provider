# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import provider.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('token', models.CharField(default=provider.utils.long_token, max_length=255, db_index=True)),
                ('expires', models.DateTimeField()),
                ('scope', models.IntegerField(default=2, choices=[(2, b'read'), (4, b'write'), (6, b'read+write')])),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('url', models.URLField(help_text=b"Your application's URL.")),
                ('redirect_uri', models.URLField(help_text=b"Your application's callback URL")),
                ('client_id', models.CharField(default=provider.utils.short_token, max_length=255)),
                ('client_secret', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('client_type', models.IntegerField(choices=[(0, b'Confidential (Web applications)'), (1, b'Public (Native and JS applications)')])),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, related_name='oauth2_client', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('code', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('expires', models.DateTimeField(default=provider.utils.get_code_expiry)),
                ('redirect_uri', models.CharField(blank=True, max_length=255)),
                ('scope', models.IntegerField(default=0)),
                ('client', models.ForeignKey(to='oauth2.Client')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('token', models.CharField(default=provider.utils.long_token, max_length=255)),
                ('expired', models.BooleanField(default=False)),
                ('access_token', models.OneToOneField(to='oauth2.AccessToken', related_name='refresh_token')),
                ('client', models.ForeignKey(to='oauth2.Client')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='client',
            field=models.ForeignKey(to='oauth2.Client'),
        ),
        migrations.AddField(
            model_name='accesstoken',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
