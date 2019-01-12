# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/23
@Author: Zhang Yafei
"""
from django.forms import ModelForm, forms
from crm import models


class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        # print('__new__',cls,args,kwargs)
        for field_name in cls.base_fields:
            file_obj = cls.base_fields[field_name]
            file_obj.widget.attrs.update({'class': 'form-control'})
            if field_name in cls.Meta.readonly_fields:
                file_obj.widget.attrs.update({'disabled':True})

        return ModelForm.__new__(cls)

    def clean(self):
        if not self.cleaned_data['contract_approved']:
            self.add_error('contract_approved','请勾选单选框')

    class Meta:
        model = models.StudentEnrollment
        # fields = ['name','consultant','status']
        fields = '__all__'
        exclude = ['contract_approved_date']
        readonly_fields = []
        # readonly_fields = ['contract_agreed']


class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        # print('__new__',cls,args,kwargs)
        for field_name in cls.base_fields:
            file_obj = cls.base_fields[field_name]
            file_obj.widget.attrs.update({'class': 'form-control'})
            if field_name in cls.Meta.readonly_fields:
                file_obj.widget.attrs.update({'disabled':True})

        return ModelForm.__new__(cls)

    def clean(self):
        if self.errors:
            raise forms.ValidationError(('Please fix errors before re-submit'))
        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance,field)
                form_val = self.cleaned_data[field]
                if old_field_val != form_val:
                    self.add_error(field,'Readonly Field:field should be "{}",not "{}"'.format(old_field_val,form_val))

    class Meta:
        model = models.CustomerInfo
        # fields = ['name','consultant','status']
        fields = '__all__'
        exclude = ['consult_content','status','consult_course']
        readonly_fields = ['contact_type','contact','consultant','referral_from',]
