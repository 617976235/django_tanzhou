# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-08 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailverify',
            options={'verbose_name_plural': '邮箱验证信息'},
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码'),
        ),
    ]
