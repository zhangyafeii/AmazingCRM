# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from kingadmin.admin_base import BaseKingAdmin


class AdminSite(object):
    def __init__(self):
        self.enable_admins = {}

    def register(self,model_class,admin_class=BaseKingAdmin):
        """注册admin表"""
        # print(model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        if not admin_class:  #为了避免多个admin_class共享同一个BaseKingAdmin对象,要实例化
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()
        admin_class.model = model_class  #把model_class赋值给了admin_class
        if app_name not in self.enable_admins:
            self.enable_admins[app_name] = {}
        self.enable_admins[app_name][model_name] = admin_class


site = AdminSite()
