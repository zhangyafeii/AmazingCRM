# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/28
@Author: Zhang Yafei
"""
from django.conf.urls import url
from teacher import views

urlpatterns = [
    url(r'^my_class$',views.my_class,name='my_class'),
]