# -*- coding: utf-8 -*-

"""
@Datetime: 2018/11/5
@Author: Zhang Yafei
"""
from crm import models
from rest_framework import serializers


# class UserSerializer(serializers.HyperlinkedModelSerializer):
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        depth = 2
        fields = ('url', 'name', 'email', 'is_staff','is_active','role')


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ('name',)

