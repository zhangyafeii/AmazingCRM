# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
import json

from django.shortcuts import render, redirect


class BaseKingAdmin(object):
    def __init__(self):
        # self.default_actions = ['delete_selected_objs']
        self.actions.extend(self.default_actions)
        self.actions = list(set(self.actions))
        # self.actions.append('delete_selected_objs')
        # print(self.actions)

    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    list_per_page = 10
    default_actions = ['delete_selected_objs']
    filter_horizontal = []
    actions = []

    def delete_selected_objs(self,request,querysets):
        # obj = querysets
        querysets_ids = json.dumps([i.id for i in querysets])
        return render(request,'kingadmin/table_obj_delete.html',{'admin_class':self,
                                                                 'objs':querysets,
                                                                 'querysets_ids':querysets_ids,
                                                                 'app_name':self.model._meta.app_label,
                                                                 'model_name':self.model._meta.model_name})
