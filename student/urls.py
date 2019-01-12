# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/28
@Author: Zhang Yafei
"""
from django.conf.urls import url
from student import views

urlpatterns = [
   url(r'^my_courses$',views.my_courses,name='my_courses'),
   url(r'^my_homework$',views.my_homework,name='my_homework'),
]