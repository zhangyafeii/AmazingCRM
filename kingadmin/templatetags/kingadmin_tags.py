# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from django.template import Library
from django.utils.safestring import mark_safe
import datetime

register = Library()


@register.simple_tag
def build_filter_ele(filter_column,admin_class):
    filter_ele = '<div class="col-md-2">{}<select class="form-control" name="{}">'.format(filter_column,filter_column)
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        for choice in column_obj.get_choices():
            selected = ''
            if filter_column in admin_class.filter_condition:#当前字段被过滤了
                if str(choice[0]) == admin_class.filter_condition.get(filter_column): #当前值被选中了
                    selected = 'selected'

            option = '<option value="{0}" {1}>{2}</option>'.format(choice[0],selected,choice[1])
            filter_ele += option
    except AttributeError as e:
        filter_ele = '<div class="col-md-2">{}<select class="form-control" name="{}__gte">'.format(filter_column,filter_column)
        if column_obj.get_internal_type() in ('DateField','DatetimeField'):
            time_obj = datetime.datetime.now()
            time_list = [
                ('','-------'),
                (time_obj,'Today'),
                (time_obj - datetime.timedelta(7),'七天内'),
                (time_obj.replace(day=1),'本月'),
                (time_obj - datetime.timedelta(90),'三个月内'),
                (time_obj.replace(month=1),'YearToDay(YTD)'),
                ('','ALL'),
            ]
            option = ''
            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else '%s-%s-%s'%(i[0].year,i[0].month,i[0].day)
                if '{}__gte'.format(filter_column) in admin_class.filter_condition:  # 当前字段被过滤了
                    if time_to_str == admin_class.filter_condition.get('{}__gte'.format(filter_column)):  # 当前值被选中了
                        selected = 'selected'
                option = '<option value="%s" %s>%s</option>'%\
                         (time_to_str,selected,i[1])
                filter_ele += option

    filter_ele += '</select></div>'
    return mark_safe(filter_ele)


@register.simple_tag
def build_table_row(obj,admin_class):
    """生成一条纪录的html element"""
    ele = ""
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):
            # column_obj = obj._meta.get_field(column_name)
            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:
                column_data = getattr(obj,'get_{}_display'.format(column_name))()
            else:
                column_data = getattr(obj,column_name)
            td_ele = '<td>{}</td>'.format(column_data)
            if index == 0:
                td_ele = '<td><a href="{}/change/">{}</a></td>'.format(obj.id,column_data)
            ele += td_ele
    else:
        td_ele = '<td><a href="{}/change/">{}</a></td>'.format(obj.id,obj)
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()


@register.simple_tag
def render_paginator(querysets,admin_class,sorted_column):
    ele = '''
        <ul class="pagination">
        '''
    #上一页
    filter_ele = render_filtered_args(admin_class)
    sorted_index = ''
    if sorted_column:
        sorted_index = '&_o={}'.format(list(sorted_column.values())[0])
    p_ele = '<li><a href="?_page=1{}{}">首页</a></li>'.format(filter_ele,sorted_index)
    ele += p_ele
    if querysets.has_previous:
        if querysets.number > 1:
            p_ele = '<li><a href="?_page={}{}{}">上一页</a></li>'.format(querysets.number-1,filter_ele,sorted_index)
        else:
            p_ele = '<li class="disabled"><a href="?_page=1{}{}">上一页</a></li>'.format(filter_ele,sorted_index)
        ele += p_ele

    #循环页码
    for i in querysets.paginator.page_range:
        active = ''
        if abs(querysets.number - i) < 2:
            if querysets.number == i:
                active = 'active'
            p_ele = '<li class="{0}"><a href="?_page={1}{2}{3}">{4}</a></li>'.format(active,i,filter_ele,sorted_index,i)
            ele += p_ele
    #下一页
    if querysets.has_next:
        if querysets.number < querysets.paginator.num_pages:
            p_ele = '<li><a href="?_page={}{}{}">下一页</a></li>'.format(querysets.number+1,filter_ele,sorted_index)
        else:
            p_ele = '<li class="disabled"><a href="?_page={}{}{}">下一页</a></li>'.format(querysets.paginator.num_pages,filter_ele,sorted_index)
        ele += p_ele
    p_ele = '<li><a>{}/{}</a></li>'.format(querysets.number,querysets.paginator.num_pages)
    ele += p_ele
    ele += '</ul>'
    return mark_safe(ele)


@register.simple_tag
def get_sorted_column(column,sorted_column,forloop):
    if column in sorted_column:#这一列被排序了
        #判断上次排序是什么顺序，本次取反
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-{}'.format(last_sort_index)

        return this_time_sort_index
    else:
        return forloop


@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    ele = ''
    if column in sorted_column:#这一列被排序了
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'top'
        else:
            arrow_direction = 'bottom'
        ele = '''<span class="glyphicon glyphicon-triangle-{}" aria-hidden="true"></span>'''.format(arrow_direction)
    return mark_safe(ele)


@register.simple_tag
def render_filtered_args(admin_class,render_html=True):
    """拼接筛选的字段"""
    ele = ''
    if admin_class.filter_condition:
        for k,v in admin_class.filter_condition.items():
            ele += '&{}={}'.format(k,v)
        if render_html:
            return mark_safe(ele)
    return ele


@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    return list(sorted_column.values())[0] if sorted_column else ''


@register.simple_tag
def get_obj_field_value(admin_class,field):
    """返回model_obj具体字段的值"""
    get_field_value = 'get_{}_display'.format(field)
    if hasattr(admin_class.instance,get_field_value):
        return getattr(admin_class.instance,get_field_value)()
    else:
        return getattr(admin_class.instance,field)


@register.simple_tag
def get_field_verbose_name(admin_class,column):
    """返回对应字段的verbose_name属性"""
    return admin_class.model._meta.get_field(column).verbose_name


@register.simple_tag
def get_available_m2m_data(field_name,form_obj,admin_class):
    """返回的是m2m字段关系关联表的所有数据"""
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = set(field_obj.related_model.objects.all())
    if form_obj.instance.id:
        selected_data = set(getattr(form_obj.instance,field_name).all())
    else:
        selected_data = set()
    # try:
    #     selected_data = set(getattr(form_obj.instance,field_name).all())
    # except TypeError:
    #     selected_data = set()
    return obj_list-selected_data


@register.simple_tag
def get_selected_m2m_data(field_name,form_obj):
    """返回已选的数据"""
    if form_obj.instance.id:
        selected_data = getattr(form_obj.instance,field_name).all()
    else:
        selected_data = None
    # try:
    #     selected_data = getattr(form_obj.instance,field_name).all()
    # except TypeError:
    #     selected_data = None
    return selected_data


@register.simple_tag
def get_model_verbose_name(admin_class):
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def get_model_verbose_name_plural(site,app_name,model_name):
    admin_class = site.enable_admins[app_name][model_name]
    return admin_class.model._meta.verbose_name_plural


@register.simple_tag
def display_all_related_objs(obj):
    """显示要删除对象的所有关联字段"""
    ele = '<ul><b style="color:red;" >{}</b>'.format(obj)
    for reverse_fk_obj in obj._meta.related_objects:
        related_table_name = reverse_fk_obj.name
        related_lookup_key = '{}_set'.format(related_table_name)
        related_objs = getattr(obj,related_lookup_key).all()  #查出所有反向关联的表
        ele += '<li>{}<ul>'.format(related_table_name)
        if reverse_fk_obj.get_internal_type() == 'ManyToManyField':  #不需要深入查找
            for i in related_objs:
                ele += '<li><a href="/kingadmin/{}/{}/{}/change" >{}</a> 记录里与[{}]相关的数据将会被删除</li>'.format(i._meta.app_label,i._meta.model_name,i.id,i,obj)
        else:
            for i in related_objs:
                ele += '<li><a href="/kingadmin/{}/{}/{}/change" >{}</a></li>'.format(i._meta.app_label,i._meta.model_name,i.id,i)
                ele += display_all_related_objs(i)

        ele += '</ul></li>'
    ele += '</ul>'
    return ele




