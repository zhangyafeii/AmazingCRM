import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from kingadmin import app_setup
from django.contrib.auth.decorators import login_required
from kingadmin.sites import site
from kingadmin.form_handle import create_dynamic_model_form
from kingadmin import permissions
from django.contrib.auth.hashers import make_password, check_password
# print('sites:',site.enable_admins)

app_setup.kingadmin_auto_discover()  #执行每个app中的kingadmin，将每一个app中注册的models添加到sites中
                                     # 的enable_admins中，并将每一个自定制的AdminSite赋值给admin_class并实例化，
                                     #admin_class.model=注册的model,这样就可以获取每一个model中的数据


def acc_login(request):
    error_msg = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/kingadmin/'))
        else:
            error_msg = 'Wrong username or password'
    return render(request,'kingadmin/login.html',{'error_msg':error_msg})


def acc_logout(request):
    logout(request)
    return redirect('kingadmin:login')


@login_required
def update_password(request):
    app_name = request.user._meta.app_label
    model_name = request.user._meta.model_name
    if request.method == 'GET':
        change_form = site.enable_admins[app_name][model_name].add_form(instance=request.user)
    else:
        print(request.POST)
        change_form = site.enable_admins[app_name][model_name].add_form(data=request.POST,instance=request.user)
        print(change_form)
        if change_form.is_valid():
            change_form.save()
            return redirect('kingadmin:login')
    return render(request,'kingadmin/update_password.html',{'form':change_form})


@login_required
def index(requeest):
    return render(requeest,'kingadmin/index.html',{'site':site})


@permissions.check_permission
def app_index(requeest):
    return render(requeest,'kingadmin/app_index.html',{'site':site})


@permissions.check_permission
def app_model_index(request,app_name):
    app_models = site.enable_admins[app_name]
    return render(request,'kingadmin/app_model_index.html',{'app_models':app_models,'app_name':app_name,'site':site})


@permissions.check_permission
def get_filter_result(request,querysets,admin_class):
    filter_condition = {}
    for key,val in request.GET.items():
        if key in ('_page','_o','_q'):continue
        if val:
            filter_condition[key] = val

    # print(filter_condition)
    return querysets.filter(**filter_condition),filter_condition


@permissions.check_permission
def get_search_result(request,querysets,admin_class):
    search_k = request.GET.get('_q')
    if search_k:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(('{}__contains'.format(search_field),search_k))

        return querysets.filter(q)
    else:
        return querysets


@permissions.check_permission
def table_obj_list(request,app_name,model_name):
    admin_class = site.enable_admins[app_name][model_name]
    if request.method == 'POST':
        # print(request.POST)
        selected_action = request.POST.get('action')
        selected_ids = json.loads(request.POST.get('selected_ids'))
        # print(selected_action,selected_ids)
        if not selected_action: #如果有action参数，代表这是一个正常的action,如果没有，代表可能是一个删除动作
            if selected_ids: #这些选中的数据都要删除
                admin_class.model.objects.filter(id__in=selected_ids).delete()
        else:  #走action流程
            selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
            admin_action_func = getattr(admin_class,selected_action)
            response = admin_action_func(request,selected_objs)
            if response:
                return response

    querysets = admin_class.model.objects.all().order_by('-id')
    querysets,filter_condition = get_filter_result(request,querysets,admin_class)
    admin_class.filter_condition = filter_condition
    #searched queryset_result
    querysets = get_search_result(request,querysets,admin_class)
    admin_class.search_key = request.GET.get('_q','')
    #sorted_querysets
    querysets,sorted_column = get_orderby_result(request,querysets,admin_class)
    # print(admin_class.model._meta.get_field('name').verbose_name)
    paginator = Paginator(querysets, admin_class.list_per_page)
    page = request.GET.get('_page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets= paginator.page(paginator.num_pages)
    return render(request,'kingadmin/table_obj_list.html',{'querysets':querysets,
                                                           'admin_class':admin_class,
                                                           'sorted_column':sorted_column,
                                                           'app_name':app_name,
                                                           'model_name':model_name,
                                                           })


@permissions.check_permission
def get_orderby_result(request,querysets,admin_class):
    """排序"""
    current_ordered_column = {}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_ordered_column[orderby_key] = orderby_index  #为了让前端知道所有排过序的列
        if orderby_index.startswith('-'):
            orderby_key = '-{}'.format(orderby_key)
        return querysets.order_by(orderby_key),current_ordered_column
    else:
        return querysets,current_ordered_column


@permissions.check_permission
def table_obj_change(request,app_name,model_name,obj_id):
    """kingadmin数据修改页"""
    admin_class = site.enable_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class)
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
        # print(dir(form_obj))
        # print(dir(form_obj.instance))
        # for field in form_obj:
            # print(dir(field))
            # print(field.name)
            # print(field.label)
            # print(field.value())
    elif request.method == 'POST':
        print(type(request.POST.get('password')))
        if request.POST.get('password',None) and len(request.POST.get('password'))!= 78:
            request.POST._mutable = True
            request.POST['password'] = make_password(request.POST.get('password'))
            request.POST._mutable = False
        print(request.POST)
        form_obj = model_form(instance=obj,data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('kingadmin:table_obj_list',app_name,model_name)

    return render(request,'kingadmin/table_obj_change.html',locals())


# @permissions.check_permission
@login_required
def table_obj_add(request,app_name,model_name):
    admin_class = site.enable_admins[app_name][model_name]
    model_form = create_dynamic_model_form(admin_class,form_add=True)
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        print(request.POST)
        if request.POST.get('password',None):
            request.POST._mutable = True
            request.POST['password'] = make_password(request.POST.get('password'))
            request.POST._mutable = False
        print(request.POST)
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('kingadmin:table_obj_list',app_name,model_name)
    return render(request,'kingadmin/table_obj_add.html',locals())


# @permissions.check_permission
@login_required
def table_obj_delete(request,app_name,model_name,obj_id):
    admin_class = site.enable_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('kingadmin:table_obj_list',app_name,model_name)
    return render(request,'kingadmin/table_obj_delete.html',locals())
