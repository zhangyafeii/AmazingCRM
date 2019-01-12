from django.shortcuts import render


def my_class(request):
    class_list = request.user.classlist_set.all()
    # for cls in class_list:
        # print(dir(cls))
        # print(cls.courserecord_set.count())
    return render(request,'teacher/my_class.html',locals())
