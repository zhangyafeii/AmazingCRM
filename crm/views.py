import json
import os
import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from crm import models, rest_serializer
from crm import forms
from django.views.decorators.csrf import csrf_exempt
from django import conf
from django.db.utils import IntegrityError
from django.contrib.auth.hashers import make_password
# from django.utils.timezone import datetime


@login_required
def dashboard(request):
    return render(request,'crm/dashboard.html')


def api_test(request):
    # data = request.POST.get('data')
    data = json.loads(request.POST.get('data'))
    serializer_obj = rest_serializer.UserSerializer(data=data)
    if serializer_obj.is_valid():
        serializer_obj.save()
    return render(request,'crm/api-test.html',locals())


@login_required
def stu_enrollment(request):
    customers = models.CustomerInfo.objects.all()
    class_list = models.ClassList.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        class_grade_id = request.POST.get('class_grade')
        try:
            enrollment_obj = models.StudentEnrollment.objects.create(customer_id=customer_id,class_grade_id=class_grade_id,consultant_id=request.user.id,)
        except IntegrityError as e:
            enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id,class_grade_id=class_grade_id)
            if enrollment_obj.contract_agreed == True:
                return redirect('contract_audit',enrollment_obj.id)
        enrollment_link = 'http://127.0.0.1:8000/crm/enrollment/{}/'.format(enrollment_obj.id)
    return render(request,'crm/stu_enrollment.html',locals())


def enrollment(request,enrollment_id):
    """学员在线报名表地址"""
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if enrollment_obj.contract_agreed == True:
        return HttpResponse('您的报名合同正在审核中！请勿重复提交')
    if request.method == 'POST':
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer,data=request.POST)
        if customer_form.is_valid():
            # print(customer_form.cleaned_data)
            customer_form.save()
            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_signed_date = datetime.datetime.now()
            enrollment_obj.save()
            return HttpResponse('您已成功提交报名信息，请等待审核通过，欢迎加入飞凡教育！')
        print(customer_form.errors)
    else:
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer)
    #列出已上传文件
    uploaded_files = []
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)
    if os.path.isdir(enrollment_upload_dir):
        uploaded_files = os.listdir(enrollment_upload_dir)

    return render(request,'crm/enrollment.html',locals())


@csrf_exempt
def enrollment_fileupload(request,enrollment_id):
    print(request.FILES)
    print(conf.settings.CRM_FILE_UPLOAD_DIR)
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    file_obj = request.FILES.get('file')
    if len(os.listdir(enrollment_upload_dir))<2:
        with open(os.path.join(enrollment_upload_dir,file_obj.name),'wb') as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        return HttpResponse(json.dumps({'status':False,'err_msg':'max_upload_limit_to_2'}))
    return HttpResponse(json.dumps({'status':True}))


def send_qq_mail(user_obj):
    email_title = 'Pyhton SMTP 邮件服务测试'
    email_body = '恭喜你成为飞凡教育的学员，您的账号为{}，密码为 feifan@123 \n请尽快登录网站修改密码。'.format(user_obj.username)
    # email = '1271570224@qq.com'  # 对方的邮箱
    send_status = send_mail(email_title, email_body, conf.settings.DEFAULT_FROM_EMAIL, [user_obj.email])
    return send_status


def contract_audit(request,enrollment_id):
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if request.method == 'POST':
        # print(request.POST)
        enrollment_form = forms.EnrollmentForm(instance=enrollment_obj,data=request.POST)
        if enrollment_form.is_valid():
            enrollment_form.save()
            stu_obj = models.Student.objects.get_or_create(customer=enrollment_obj.customer)[0]
            stu_obj.class_grade.add(enrollment_obj.class_grade_id)
            stu_obj.save()
            enrollment_obj.customer.status = 1
            enrollment_obj.save()

            user_obj = User.objects.get_or_create(username=enrollment_obj.customer.contact,password=make_password('feifan@123',None,'pbkdf2_sha256'),email=enrollment_obj.eamil_address)[0]
            user_profile_obj = models.UserProfile.objects.get_or_create(user=user_obj,name=enrollment_obj.customer.name,student_id=stu_obj.id)[0]
            role_obj = models.Role.objects.get(name='students')
            user_profile_obj.role.add(role_obj)
            user_profile_obj.save()

            send_status = send_qq_mail(user_obj)
            return redirect('kingadmin:table_obj_change','crm','student',stu_obj.id)
    else:
        customer_form = forms.CustomerForm(instance=enrollment_obj.customer)
        enrollment_form = forms.EnrollmentForm(instance=enrollment_obj)
    return render(request,'crm/contract_audit.html',locals())


@csrf_exempt
def enrollment_file_delete(request,enrollment_id):
    result = {'status':True,'message':None}
    file_name = request.POST.get('file_name')
    enrollment_upload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR, enrollment_id)
    print(enrollment_upload_dir)
    file_path = os.path.join(enrollment_upload_dir,file_name)
    print(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        result['status'] = False
        result['message'] = '文件不存在或已删除，请尝试刷新本页面'
    return JsonResponse(result)