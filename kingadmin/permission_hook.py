# -*- coding: utf-8 -*-

"""
@Datetime: 2018/11/1
@Author: Zhang Yafei
"""


def view_my_own_customers(request):
    print('running permisssion hook check...')
    if str(request.user.id) == request.GET.get('consultant'):
        print('访问自己创建的用户，允许')
        return True
    else:
        return False