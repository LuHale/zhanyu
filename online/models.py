#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):#creat user fields
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=50)
	
class account(models.Model):#creat user_account fields
	user = models.CharField(max_length=50)
	userdate = models.CharField(max_length=50)
	usetimes = models.CharField(max_length=20)
	times = models.CharField(max_length=20)
	group = models.CharField(max_length=6)
	money = models.CharField(max_length=20)
	tag = models.CharField(max_length=20)
	
	def __unicode__(self):
		return self.user

#class group(models.Model):
	#groupid = models.AutoField(primary_key=True)

class groupcreater (models.Model):#创建俱乐部的用户和俱乐部id匹配
	groupid = models.ForeignKey(Group)
	userid = models.ForeignKey(User)
	creatdate = models.CharField(max_length=30)
	
class user_group(models.Model):
	groupid = models.ForeignKey(Group)
	userid = models.ForeignKey(User)
	join_date = models.CharField(max_length=30)