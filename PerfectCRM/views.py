# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def acc_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username=username,password=password)
        print(user)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/kingadmin/'))
        else:
            error_msg = 'Wrong username or password'
    return render(request,'login.html',{'error_msg':error_msg})


def acc_logout(request):
    logout(request)
    return redirect('login')