# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ia', '0003_auto_20170509_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userperfil',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='up_perfiles', to='ia.Perfil'),
        ),
        migrations.AlterField(
            model_name='userperfil',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='up_usuarios', to=settings.AUTH_USER_MODEL),
        ),
    ]
