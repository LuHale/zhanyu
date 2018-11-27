# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-07-13 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('userdate', models.CharField(max_length=50)),
                ('usetimes', models.CharField(max_length=20)),
                ('times', models.CharField(max_length=20)),
                ('group', models.CharField(max_length=6)),
                ('money', models.CharField(max_length=20)),
                ('tag', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='groupcreater',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creatdate', models.CharField(max_length=30)),
                ('groupid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='user_group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.CharField(max_length=30)),
                ('groupid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online.User')),
            ],
        ),
        migrations.AddField(
            model_name='groupcreater',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online.User'),
        ),
    ]