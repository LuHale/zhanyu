#coding=utf-8
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.template import loader


def sendmail(club,name,date,usetimes,times): 
	club = club
	username = name
	date = date
	usetimes = usetimes
	times = times
	to_email = User.objects.filter(username=username)[0].email
	user = User.objects.filter(username=username)[0].last_name + User.objects.filter(username=username)[0].first_name
	print user
	from_email = settings.DEFAULT_FROM_EMAIL
	subject = club + '消费记录'
	text_content = ''
	html_content = loader.render_to_string(
                     'mail.html',               #需要渲染的html模板
                     {
						'club':club,
                        'username':user, 						#参数
						'datetime':date, 
						'usetimes':usetimes, 
						'times':times
                     }
               )
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
	msg.attach_alternative(html_content, "text/html")
	msg.send()
