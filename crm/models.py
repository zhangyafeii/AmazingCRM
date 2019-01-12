from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    """用户信息表"""
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=64,verbose_name='姓名')
    role = models.ManyToManyField('Role',blank=True)
    student = models.OneToOneField('Student',blank=True,null=True,on_delete=models.CASCADE)
    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '用户表'
        permissions = (
            ('crm_app_index','可以访问kingadmin首页'),
            ('crm_app_model_index','查看app里的model'),
            ('crm_table_obj_list','可以查看kingadmin每张表里所有的数据'),
            ('crm_table_list_view','可以访问kingadmin每张表里每条数据的修改页'),
            ('crm_table_list_change','可以对kingadmin每张表的数据进行修改'),
            ('crm_table_obj_add_view','可以访问kingadmin数据增加页'),
            ('crm_table_obj_add','可以对kingadmin里每张表进行数据添加'),
            ('crm_table_obj_delete_view', '可以访问kingadmin数据删除页'),
            ('crm_table_obj_delete','可以对kingadmin的表里的数据进行删除'),
        )
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

#
# class UserProfile(models.Model):
#     """用户信息表"""
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=64,verbose_name='姓名')
#     role = models.ManyToManyField('Role',blank=True)
#     student = models.OneToOneField('Student',blank=True,null=True,on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name
#
#     #admin中显示表名称
#     class Meta:
#         verbose_name_plural = '用户信息表'


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64,unique=True)
    menus = models.ManyToManyField('Menus',blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '角色表'


class CustomerInfo(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=64,default=None,verbose_name='姓名')
    contact_type_choices = [(0,'qq'),(1,'微信'),(2,'手机')]
    contact_type = models.SmallIntegerField(choices=contact_type_choices,default=0,verbose_name='联系方式类型')
    contact = models.CharField(max_length=64,unique=True,verbose_name='联系方式')

    source_choices = [(0,'QQ群'),(1,'51CTO'),(2,'百度推广'),(3,'知乎'),(4,'转介绍'),(5,'其他'),]
    source = models.SmallIntegerField(choices=source_choices,verbose_name='来源')
    referral_from = models.ForeignKey('self',blank=True,null=True,verbose_name='转介绍',on_delete=models.SET_NULL)

    consult_courses = models.ManyToManyField('Course',verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')

    status_choices = [(0,'未报名'),(1,'已报名'),(2,'已退学')]
    status = models.SmallIntegerField(choices=status_choices,verbose_name='状态')

    consultant = models.ForeignKey(UserProfile,verbose_name='课程顾问',on_delete=models.CASCADE)
    id_num = models.CharField(verbose_name='身份证号',max_length=128,blank=True,null=True)
    emergence_contact = models.PositiveIntegerField(verbose_name='现有联系方式',blank=True,null=True)
    sex_choices = ((0,'男'),(1,'女'))
    sex = models.PositiveIntegerField(verbose_name='性别',choices=sex_choices,blank=True,null=True)
    date = models.DateField(auto_now_add=True,verbose_name='日期')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '客户信息表'


class Student(models.Model):
    """学员表"""
    customer = models.OneToOneField('CustomerInfo',on_delete=models.CASCADE)
    class_grade = models.ManyToManyField('ClassList')

    def __str__(self):
        return self.customer.name

    class Meta:
        verbose_name_plural = '学员表'


class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey(CustomerInfo,on_delete=models.CASCADE)
    content = models.TextField(verbose_name='跟踪内容')
    user = models.ForeignKey('UserProfile',verbose_name='跟进人',on_delete=models.CASCADE)
    status_choices = [(0,'近期无报名计划'),(1,'一个月内报名'),(2,'2轴内报名'),(3,'已报名'),]
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '客户跟踪记录表'


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64,unique=True,verbose_name='课程名称')
    price = models.PositiveIntegerField(verbose_name='价格')
    period = models.PositiveIntegerField(verbose_name='课程周期（月）',default=5)
    outline = models.TextField(verbose_name='大纲')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '课程表'


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch',on_delete=models.CASCADE,verbose_name='校区')
    course = models.ForeignKey('Course',on_delete=models.CASCADE,verbose_name='课程')
    day_nums = models.PositiveIntegerField(verbose_name='课程总节次',default=10)
    class_type_choices = [(0,'脱产'),(1,'周末'),(2,'网络班')]
    class_type = models.SmallIntegerField(choices=class_type_choices,default=0,verbose_name='班级类型')
    semester = models.SmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField('UserProfile',verbose_name='讲师')
    start_date = models.DateField('开班日期')
    graduate_date = models.DateField('毕业日期',blank=True,null=True)
    contract_template = models.ForeignKey('ContractTemplate',blank=True,null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return '{}({})期'.format(self.course.name,self.semester)

    class Meta:
        unique_together = ('course','class_type','semester','branch')
        verbose_name_plural = '班级列表'


class CourseRecord(models.Model):
    """上课记录表"""
    class_grade = models.ForeignKey('ClassList',verbose_name='上课班级',on_delete=models.CASCADE)
    day_num = models.PositiveIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    title = models.CharField(max_length=64,verbose_name='本节主题')
    content = models.TextField('本节内容')
    has_homework = models.BooleanField('本节有作业',default=True)
    homework = models.TextField('作业要求',blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True,verbose_name='课程时间')

    def __str__(self):
        return '{}第{}节'.format(self.class_grade,self.day_num)

    class Meta:
        unique_together = ('class_grade','day_num')
        verbose_name_plural = '上课记录表'


class StudyRecord(models.Model):
    """学习记录表"""
    course_record = models.ForeignKey('CourseRecord',on_delete=models.CASCADE)
    student = models.ForeignKey('Student',on_delete=models.CASCADE)

    score_choices = [(100,'A+'),
                     (90,'A'),
                     (85,'B+'),
                     (80,'B'),
                     (75,'B-'),
                     (70,'C+'),
                     (60,'C'),
                     (40,'C-'),
                     (-50,'D'),
                     (0,'N/A'), #not avaliable
                     (-100,'COPY'),
                     ]
    score = models.SmallIntegerField(choices=score_choices,default=0)
    show_choices = [(0,'缺勤'),
                    (1,'已签到'),
                    (2,'迟到'),
                    (3,'早退'),
                    ]
    show_status = models.SmallIntegerField(choices=show_choices,default=1)
    note = models.CharField('成绩备注',max_length=64,blank=True,null=True)

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.course_record,self.student,self.score)

    class Meta:
        verbose_name_plural = '学习记录表'


class Branch(models.Model):
    """校区表"""
    name = models.CharField(max_length=64,unique=True)
    addr = models.CharField(max_length=64,blank=True,null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '校区'


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = ((0,'absoule'),(1,'dynamic'))
    url_type = models.SmallIntegerField(choices=url_type_choices,default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        """联合唯一"""
        unique_together = ('name','url_name')
        verbose_name_plural = '菜单'


class ContractTemplate(models.Model):
    """存储合同模板"""
    name = models.CharField(max_length=64)
    content = models.TextField()

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '合同模板'


class StudentEnrollment(models.Model):
    """学员报名表"""
    customer = models.ForeignKey('CustomerInfo',on_delete=models.CASCADE)
    class_grade = models.ForeignKey('ClassList',on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    eamil_address = models.EmailField(default=None)
    contract_agreed = models.BooleanField(default=False)
    contract_signed_date = models.DateTimeField(blank=True,null=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateTimeField(verbose_name='合同审核时间',blank=True,null=True)

    def __str__(self):
        return self.customer.name

    class Meta:
        unique_together = ('customer','class_grade')
        verbose_name_plural = '学员报名表'


class PaymentRecord(models.Model):
    """存储学员缴费记录"""
    enrollment = models.ForeignKey(StudentEnrollment,on_delete=models.CASCADE)
    payment_type_choices = ((0,'报名费'),(1,'学费'),(2,'退费'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices)
    amount = models.PositiveIntegerField('费用',default=500)
    consultant = models.ForeignKey(UserProfile,on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.enrollment

    class Meta:
        verbose_name_plural = '学员缴费记录表'