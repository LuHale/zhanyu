#coding=utf-8
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django import forms
from models import User
from models import account
from django.views.decorators.csrf import csrf_exempt
import time
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from models import groupcreater,user_group

from email import sendmail

class UserForm(forms.Form):
	username = forms.CharField(label=u'用户名',max_length=100)
	password = forms.CharField(label=u'密码',widget=forms.PasswordInput())
	email = forms.CharField(label=u'邮箱',max_length=254)
	last_name = forms.CharField(label=u'姓',max_length=30)
	first_name = forms.CharField(label=u'名',max_length=30)


class UserForm_login(forms.Form):
	username = forms.CharField(label=u'用户名',max_length=100)
	password = forms.CharField(label=u'密码',widget=forms.PasswordInput())
	
def regist(req):
	if req.method == 'POST':
		uf = UserForm(req.POST)
		if uf.is_valid():
			username = uf.cleaned_data['username']
			password = uf.cleaned_data['password']
			email = uf.cleaned_data['email']
			last_name = uf.cleaned_data['last_name']
			first_name = uf.cleaned_data['first_name']
			user = User.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name)
			user.save()
			return HttpResponseRedirect('/online/login/')
	else:
		uf = UserForm()
	return render_to_response('regist.html',{'uf':uf},context_instance=RequestContext(req))

def login_view(req):
		if req.method == 'POST':
			uf = UserForm_login(req.POST)
			if uf.is_valid():
				username = uf.cleaned_data['username']
				password = uf.cleaned_data['password']
				user = authenticate(username=username,password=password)  #验证用户账号和密码，返回用户对象
				if user is not None:#如果用户验证成功
					if user.is_active:#如果用户账号为激活状态
						login(req,user)
						response = HttpResponseRedirect('/online/index/')
						response.set_cookie('username',username,3600)
						return response
					else:
						return HttpResponse('用户为不可用状态!!')
				else:
					return HttpResponseRedirect('/online/login/')
		else:
			uf = UserForm_login()
		return render_to_response('login.html',{'uf':uf},context_instance=RequestContext(req))

def index(req):#显示所有数据
	#校验登陆用户
	username = req.COOKIES.get('username','')
	print username
	if username :
	#return render_to_response('index.html',{'username':username})
		#显示用户管理的俱乐部信息
		itemslist = {}
		ud = User.objects.filter(username=username)[0].id#找到当前登录用户id
		print ud
		gc = groupcreater.objects.filter(userid_id=ud)#找到当前用户创建的组的列表
		if gc:
			for eachgroup in gc:#循环显示创建的组
				gd = eachgroup.groupid_id
				UserInGroup = user_group.objects.filter(groupid_id=gd)
				groupname = Group.objects.filter(id=gd)[0].name
				itemslist[groupname] = ''
				users = []
				if UserInGroup:#如果某一组对应有用户
					for eachuser in UserInGroup:
						ud = eachuser.userid_id#取出用户id
						un = User.objects.filter(id=ud)[0].username
						userinfo = account.objects.filter(user=un).filter(group=gd)
						users += userinfo
				itemslist[groupname] = users
		#itemslist = account.objects.all()
		#显示用户加入的俱乐部的消费信息
		ud = User.objects.filter(username=username)[0].id
		ug = user_group.objects.filter(userid_id=ud)
		groupcreaterlist = groupcreater.objects.filter(userid_id=ud)

		grouplist = []
		groupjoindict = {}
		if groupcreaterlist:#如果用户创建了组
			for eachowner in groupcreaterlist:
				gcid = eachowner.groupid_id
				grouplist.append(gcid)
		if ug:#如果用户加入了组
			for eachgroup in ug:
				usergroupid = eachgroup.groupid_id
				groupname = Group.objects.filter(id=usergroupid)[0].name
				if usergroupid not in grouplist:#去掉用户自己创建的组
					useraccount = account.objects.filter(group=usergroupid).filter(user=username)#查询用户加入的组
					groupjoindict[groupname] = useraccount

			
		return render_to_response('index.html',{'userinfo':itemslist,'usergrouplist':groupjoindict,'username':username,'ifgroupcreater':gc})
	else:
		return HttpResponseRedirect('/online/login/')
"""
def query(req):
	itemslist = account.objects.all()
	return render_to_response('index.html',{'userinfo':itemslist})
"""
def delete(req):  #删除数据库对应id的信息
	username = req.COOKIES.get('username','')
	if username :
		id = req.GET['id']
		groupname = req.GET['groupname']
		gd = Group.objects.filter (name=groupname)[0].id
		bb = account.objects.filter(id=id).filter(group=gd)
		bb.delete()
		return HttpResponseRedirect('/online/index/')
	else:
		return HttpResponseRedirect('/online/login/')

def update(req):#更新数据
    #id = req.POST['id']
	
	username = req.COOKIES.get('username','')
	if username :#如果用户登录就进行添加用户操作
		user = req.GET['user']
		groupname = req.GET['groupname']
		datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		if req.method == 'POST':
			gname = req.POST.get('clubname')
			name = req.POST.get('sname')
			date = req.POST.get('sdate')
			usetimes = req.POST.get('susetimes')
			times = req.POST.get('stimes')
			ua = account()
			if len(name) != 'Null':
				#ua.id = id
				gd = Group.objects.filter(name=gname)[0].id
				ua.group = gd
				ua.userdate = date
				ua.user = name
				ua.usetimes = usetimes
				ua.times = times
				ua.save()
				sendmail(gname,name,date,usetimes,times)
				#发送邮件通知
				return HttpResponseRedirect('/online/index/')
		return render_to_response('update.html',{'unm':user,'groupname':groupname,'datetime':datetime},context_instance=RequestContext(req))
	else:
		return HttpResponseRedirect('/online/login/')

def show(req):
	username = req.COOKIES.get('username','')
	if username :
		user = req.GET['user']
		groupname = req.GET['groupname']
		gd = Group.objects.filter (name=groupname)[0].id
		bb = account.objects.filter(user=user).filter(group=gd)
		return render_to_response('show.html',{'data':bb,'user':user})
	else:
		return HttpResponseRedirect('/online/login/')

def logout(req):
	#response = HttpResponse('logout!!')
	#response.delete_cookie('username')
	response = HttpResponseRedirect('/online/login/')
	response.delete_cookie('username')
	return response

def creatgroups(req):#创建俱乐部
	username = req.COOKIES.get('username','')
	if username :
		if req.method == 'POST':
			name = req.POST.get('clubname')
			ug = Group()
			if len(name) != 'Null':
				#ua.id = id
				ug.name = name
				ug.save()
				#关联group表和groupcreater表（外键可能写的不对删除group数据后，groupcreater表没有对应删除）
				gd = Group.objects.filter(name=name)[0].id
				ud = User.objects.filter(username=username)[0].id
				date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
				groupcreater.objects.create(groupid_id=gd,userid_id=ud,creatdate=date)
				user_group.objects.create(groupid_id=gd,userid_id=ud,join_date=date)#添加用户到user_group表
				#groupcreater().save()
				#sendmail(name,date,usetimes,times)
				#发送邮件通知
				return HttpResponseRedirect('/online/index/')
			
		return render_to_response('creatgroups.html',context_instance=RequestContext(req))
	else:
		return HttpResponseRedirect('/online/login/')
	
def joingroups(req):
	username = req.COOKIES.get('username','')
	if username :
		groupdict = {}
		allgroups = Group.objects.all()
		for each in allgroups:
			groupname = each.name
			gd = each.id
			ud = groupcreater.objects.filter(groupid_id=gd)[0].userid_id
			creatername = User.objects.filter(id=ud)[0].last_name + User.objects.filter(id=ud)[0].first_name

			groupdict[groupname] = creatername
		return render_to_response('joingroups.html',{'groupinfo':groupdict,'user':username})
	else:
		return HttpResponseRedirect('/online/login/')
	
def joinin(req):
	username = req.COOKIES.get('username','')
	if username :
		user = username
		groupname = req.GET['group']
		ud = User.objects.filter(username=username)[0].id
		gd = Group.objects.filter(name=groupname)[0].id
		date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
		user_group.objects.create(groupid_id=gd,userid_id=ud,join_date=date)#添加用户到user_group表
		return HttpResponseRedirect('/online/index/')
		#发送邮件通知
	else:
		return HttpResponseRedirect('/online/login/')	

def adduser(req):
	username = req.COOKIES.get('username','')
	if username :
		groupname = req.GET['group']
		userlist = []
		nowuser = User.objects.filter(username=username)[0].id
		gd = Group.objects.filter(name=groupname)[0].id
		ud = user_group.objects.filter(groupid_id=gd)
		ifgroupcreater = 0
		if groupcreater.objects.filter(userid_id=nowuser).filter(groupid_id=gd):
			ifgroupcreater = 1
		for eachuser in ud:
			userid = eachuser.userid_id
			username = User.objects.filter(id=userid)[0].username
			userlist.append(username)
		print userlist
		return render_to_response('adduser.html',{'userinfo':userlist,'groupname':groupname,'ifgroupcreater':ifgroupcreater})
		#发送邮件通知
	else:
		return HttpResponseRedirect('/online/login/')	
	
	
	
	