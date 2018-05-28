#  -*- coding:utf-8 -*-

from django.core.mail import send_mail
from random import Random

from users.models import EmailVerify
from tanzhou.settings import EMAIL_FROM


# 生成一个8位数的随机字符串
def random_str(random_length=8):
    str_random = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlNnMmOoPpQqRrSsTtUuVvWwXxYyZz012346789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str_random += chars[random.randint(0, length)]
    return str_random


# 发送邮件
def send_register_email(email, send_type='register'):
    # 生成16位的验证码
    code = random_str(16)

    # 保存验证码
    email_record = EmailVerify()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    # 设置邮箱的发送信息
    if send_type == 'register':
        email_title = '潭州课堂用户注册激活链接'
        email_body = '请点击此链接激活你的账号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    if send_type == 'forget':
        email_title = '潭州课堂用户密码找回链接'
        email_body = '请点击此链接找回你的密码:http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
