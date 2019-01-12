# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/20
@Author: Zhang Yafei
"""
from django.conf.urls import url
from kingadmin import views

app_name = 'kingadmin'

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^app_index$',views.app_index,name='app_index'),
    url(r'^login$',views.acc_login,name='login'),
    url(r'^logout$',views.acc_logout,name='logout'),
    url(r'^update_password$',views.update_password,name='update_password'),
    url(r'^(\w+)/$',views.app_model_index,name='app_model_index'),
    url(r'^(\w+)/(\w+)/$',views.table_obj_list,name='table_obj_list'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_obj_change,name='table_obj_change'),
    url(r'^(\w+)/(\w+)/add$',views.table_obj_add,name='table_obj_add'),
    url(r'^(\w+)/(\w+)/(\d+)/delete$',views.table_obj_delete,name='table_obj_delete'),
]