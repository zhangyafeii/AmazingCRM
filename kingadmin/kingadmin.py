# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/28
@Author: Zhang Yafei
"""
from django.contrib.auth.models import User,Group
# from django.contrib.auth import get_user_model
from kingadmin import sites

sites.site.register(User)
sites.site.register(Group)
