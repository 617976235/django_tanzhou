from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class UserInfo(AbstractUser):
    """
      用户信息数据表
    """
    nickname = models.CharField(max_length=50, verbose_name="昵称")
    birthday = models.DateField(null=True, blank=True, verbose_name="生日")
    gender = models.CharField(max_length=10, choices=(("male", "男"), ("female", "女")),
                              default="female", verbose_name="性别")
    image = models.ImageField(upload_to="user_image/%Y/%m",
                              max_length=100, default="", verbose_name="头像")
    phone = models.CharField(null=True, blank=True, max_length=11, verbose_name="手机号码")
    qq = models.IntegerField(null=True, blank=True, verbose_name="QQ号码")
    description = models.CharField(null=True, blank=True, max_length=150, verbose_name="用户简介")

    class Meta:
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.username


class EmailVerify(models.Model):
    """
      邮箱验证数据表
    """
    email = models.EmailField(max_length=30, verbose_name="邮箱")
    code = models.CharField(max_length=20, verbose_name="验证码")
    send_type = models.CharField(max_length=10, choices=(("register", "注册"), ("reset", "找回密码")),
                                 verbose_name="类型")
    send_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name_plural = "邮箱验证信息"

    def __str__(self):
        return "{0}({1})".format(self.code, self.email)


class SlideShow(models.Model):
    name = models.CharField(max_length=30, verbose_name="轮播图名称")
    image = models.ImageField(upload_to="slide_show/%Y/%m",
                              default="", verbose_name="轮播图")
    url = models.URLField(max_length=100, verbose_name="访问地址")
    index = models.IntegerField(default=0, verbose_name="轮播顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name_plural = "轮播图"

    def __str__(self):
        return self.name

