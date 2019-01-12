# -*- coding: utf-8 -*-

"""
@Datetime: 2018/11/5
@Author: Zhang Yafei
"""
from crm import models
from rest_framework import viewsets
from crm.rest_serializer import UserSerializer,RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = UserSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = RoleSerializer

