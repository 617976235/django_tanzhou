from django.db import models
from datetime import datetime
from users.models import UserInfo


# Create your models here.


class CourseClass(models.Model):
    """
      第一分类数据表
    """
    name = models.CharField(max_length=15,
                            choices=(("it", "IT互联网"), ("language", "语言学习"), ("design", "创意设计"),
                                     ("life", "兴趣生活"), ("plant", "生产种植"), ("edu", "升学考研"),
                                     ("certificate", "公培考证")),
                            verbose_name="课程分类")

    class Meta:
        verbose_name_plural = "课程第一分类"

    def __str__(self):
        # 显示外键的中文名称
        return self.get_name_display()


class CourseSort(models.Model):
    """
      第二分类数据表
    """
    classes = models.ForeignKey(CourseClass, verbose_name="第一分类")
    name = models.CharField(max_length=50, verbose_name="第二分类")

    class Meta:
        verbose_name_plural = "课程第二分类"

    def __str__(self):
        return self.name


class Course(models.Model):
    """
      课程信息数据表
    """
    sort = models.ForeignKey(CourseSort, verbose_name="课程分类")
    name = models.CharField(max_length=30, verbose_name="课程名称")
    price = models.CharField(max_length=10, verbose_name="课程价格")
    learn_time = models.CharField(max_length=6, verbose_name="学习时长")
    buy_nums = models.IntegerField(default=0, verbose_name="购买人数")
    image = models.ImageField(upload_to="course_image/%Y/%m", verbose_name=u"课程封面图")
    describe = models.CharField(max_length=400, verbose_name="课程描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击人数")

    class Meta:
        verbose_name_plural = "课程信息"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
       课程章节信息
    """
    lesson_course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=40, verbose_name="课程章节")
    lesson_time = models.DateTimeField(default=datetime.now, verbose_name="章节时间")

    class Meta:
        verbose_name_plural = "课程章节信息"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """
       教师信息
    """
    teacher_course = models.ForeignKey(Course, verbose_name="课程名")
    teacher_name = models.CharField(max_length=30, verbose_name="教师名称")
    teacher_des = models.CharField(max_length=100, verbose_name="教师描述")
    teacher_image = models.ImageField(upload_to="teacher_image/%Y/%m", verbose_name="教师头像")

    class Meta:
        verbose_name_plural = "教师信息"

    def __str__(self):
        return self.teacher_name


class Buy(models.Model):
    """
       课程购买信息
    """
    user = models.ForeignKey(UserInfo, verbose_name="用户")
    course = models.ForeignKey(Course, verbose_name="课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")

    class Meta:
        verbose_name_plural = "课程购买信息"

    def __str__(self):
        return self.user
