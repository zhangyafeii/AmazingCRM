# -*- coding: utf-8 -*-

"""
@Datetime: 2018/10/23
@Author: Zhang Yafei
"""
from django.forms import ModelForm


def create_dynamic_model_form(admin_class,form_add=False):
    """
    动态生成modelform
    form_add False 默认是修改的表单，True时为添加
    """
    class Meta:
        model = admin_class.model
        fields = '__all__'
        if not form_add: #change
            exclude = admin_class.readonly_fields
            admin_class.form_add = False  #这是因为admin_class实例自始至终都是同一个，
            # 这里修改属性为False是为了避免上一次添加调用将其改为了True
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        # print('__new__',cls,args,kwargs)
        for field_name in cls.base_fields:
            file_obj = cls.base_fields[field_name]
            file_obj.widget.attrs.update({'class':'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     file_obj.widget.attrs.update({'disabled':True})

        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm',(ModelForm,),{'Meta':Meta,'__new__':__new__})
    # print(dynamic_form)
    return dynamic_form