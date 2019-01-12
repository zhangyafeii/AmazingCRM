# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from kingadmin import sites
from student import models
from kingadmin.admin_base import BaseKingAdmin

print('student kingadmin.....')


class TestAdmin(BaseKingAdmin):
    list_display = ['name',]


sites.site.register(models.Test,TestAdmin)