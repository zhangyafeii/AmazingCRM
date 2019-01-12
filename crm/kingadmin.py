# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/21
@Author: Zhang Yafei
"""
from kingadmin import sites
from crm import models
from kingadmin.admin_base import BaseKingAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

print('crm kingadmin.....')


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    def __new__(cls, *args, **kwargs):
        # print('__new__',cls,args,kwargs)
        for field_name in cls.base_fields:
            file_obj = cls.base_fields[field_name]
            file_obj.widget.attrs.update({'class': 'form-control'})

        return forms.ModelForm.__new__(cls)

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码不一致")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  #将明文密码 转化为密文
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseKingAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_superuser')
    list_filter = ('is_superuser',)

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    search_fields = ('email',)
    # ordering = ('email',)
    filter_horizontal = ('role','user_permissions')


class CustomerAdmin(BaseKingAdmin):
    list_display = ['id','name','source','contact_type','contact','consultant','consult_content','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name']
    readonly_fields = ['status','contact']
    # list_per_page = 10
    filter_horizontal = ['consult_courses']
    actions = ['change_status']

    def change_status(self, request, queryset):
        # print('admin_action', self, request, queryset)
        queryset.update(status=0)


class StudentAdmin(BaseKingAdmin):
    filter_horizontal = ['class_grade']


sites.site.register(models.CustomerInfo,CustomerAdmin)
sites.site.register(models.UserProfile,UserProfileAdmin)
sites.site.register(models.Role)
sites.site.register(models.Student,StudentAdmin)
sites.site.register(models.CustomerFollowUp)
sites.site.register(models.ClassList)
sites.site.register(models.Course)
sites.site.register(models.CourseRecord)
sites.site.register(models.StudyRecord)
sites.site.register(models.Branch)
sites.site.register(models.Menus)
sites.site.register(models.ContractTemplate)
sites.site.register(models.StudentEnrollment)
sites.site.register(models.PaymentRecord)
