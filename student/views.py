from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crm import models


@login_required
def my_courses(request):
    class_obj = request.user.student.class_grade.first()
    print(dir(class_obj._meta))
    print(class_obj._meta.fields)
    return render(request,'student/my_courses.html',locals())


@login_required
def my_homework(request):
    class_obj = request.user.student.class_grade.first()
    course_record = models.CourseRecord.objects.get(class_grade=class_obj)
    study_record = models.StudyRecord.objects.filter(course_record=course_record)
    return render(request, 'student/my_homework.html', locals())

