# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/20
@Author: Zhang Yafei
"""
from django.conf.urls import url,include
from crm import views
from crm.rest_views import UserViewSet,RoleViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'roles', RoleViewSet)


urlpatterns = [
    url(r'^$',views.dashboard,name='sales_dashboard'),
    url(r'^api/', include(router.urls),name='api'),
    url(r'^apitest$', views.api_test,name='api_test'),
    url(r'^stu_enrollment$',views.stu_enrollment,name='stu_enrollment'),
    url(r'^enrollment/(\d+)/$',views.enrollment,name='enrollment'),
    url(r'^enrollment/(\d+)/fileupload$',views.enrollment_fileupload,name='enrollment_fileupload'),
    url(r'^stu_enrollment/(\d+)/contract_audit/$',views.contract_audit,name='contract_audit'),
    url(r'^enrollment/(\d+)/file_delete$',views.enrollment_file_delete,name='enrollment_file_delete'),
]