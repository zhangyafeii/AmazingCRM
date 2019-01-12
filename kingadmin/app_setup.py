# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from django import conf
import importlib


def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        try:
            #方式一： mod1 = importlib.import_module(app_name,'kingadmin')
            mod = __import__('{}.kingadmin'.format(app_name)) #方式二
            print(mod.kingadmin)
        except:
            pass