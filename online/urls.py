"""online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns,url
from online import views

urlpatterns = [
    url(r'^$', views.login_view,name='login_view'),
	url(r'^login/$',views.login_view,name='login_view'),
	url(r'^regist/$',views.regist,name='regist'),
	url(r'^index/$',views.index,name='index'),
	url(r'^logout/$',views.logout,name='logout'),
	url(r'^delete/$',views.delete,name='delete'),
	url(r'^update/$',views.update,name='update'),
	url(r'^show/$',views.show,name='show'),
	url(r'^creatgroups',views.creatgroups,name='creatgroups'),
	url(r'^joingroups',views.joingroups,name='joingroups'),
	url(r'^joinin',views.joinin,name='joinin'),
	url(r'^adduser',views.adduser,name='adduser'),
]