# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/30
@Author: Zhang Yafei
"""
from kingadmin import permission_hook

perm_dic = {
    # 'crm_table_index': ['table_index', 'GET', ['source','status',], {'source':'qq',}, ],  # 可以查看CRM APP里所有数据库表
    'crm_app_index':['app_index','GET',[],{}],
    'crm_app_model_index':['app_model_index','GET',[],{}],  #查看app里的model
    'crm_table_obj_list': ['table_obj_list', 'GET', [], {}],  # 可以查看每张表里所有的数据
    # 'crm_table_obj_list': ['table_obj_list', 'GET', [], {}, permission_hook.view_my_own_customers],  # 可以查看每张表里所有的数据
    'crm_table_list_view': ['table_obj_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
    'crm_table_list_change': ['table_obj_change', 'POST', [], {}],  # 可以对每张表里的数据修改
    'crm_table_obj_add_view': ['table_obj_add', 'GET', [], {}],  # 可以访问数据增加页
    'crm_table_obj_add': ['table_obj_add', 'POST', [], {}],  # 可以创建表里的数据
    'crm_table_obj_delete_view': ['table_obj_delete', 'GET', [], {}],  # 可以访问删除页
    'crm_table_obj_delete': ['table_obj_delete', 'POST', [], {}],  # 可以对表里的数据进行删除
}

"""
装饰器
"""
