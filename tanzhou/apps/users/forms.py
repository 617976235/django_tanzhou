from django import forms
from captcha.fields import CaptchaField


# 登录验证
class LoginForm(forms.Form):
    username = forms.CharField(required=True,
                               min_length=3,
                               max_length=20,
                               error_messages={'required': '用户名不能为空.',
                                               'min_length': '用户名不能小于3个字符.',
                                               'max_length': '用户名不能大于20个字符.'})
    password = forms.CharField(required=True,
                               min_length=3,
                               max_length=20,
                               error_messages={'required': '密码不能为空.',
                                               'min_length': '密码不能小于3个字符.',
                                               'max_length': '密码不能大于20个字符.'})


# 注册验证
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,
                             error_messages={'required': '邮箱不能为空.'})
    password = forms.CharField(required=True,
                               min_length=6,
                               error_messages={'required': '密码不能为空.', 'min_length': '密码不能少于6位数字.'})
    captcha = CaptchaField(required=True,
                           error_messages={'required': '验证码不能为空.', 'invalid': '验证码错误.'})
