from django import forms
# 引入图形验证码的字段
from captcha.fields import CaptchaField
from users.models import UserInfo


# 登录表单
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


# 注册表单
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True,
                             error_messages={'required': '邮箱不能为空.'})
    password = forms.CharField(required=True,
                               min_length=6,
                               error_messages={'required': '密码不能为空.',
                                               'min_length': '密码不能少于6位数字.'})
    captcha = CaptchaField(required=True,
                           error_messages={'required': '验证码不能为空.',
                                           'invalid': '验证码错误.'})


# 忘记密码表单
class ForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True,
                             error_messages={'required': '邮箱不能为空.'})
    captcha = CaptchaField(required=True,
                           error_messages={'invalid': '验证码错误',
                                           'required': '验证码不能为空.'})


# 找回密码-重置密码表单
class ResetPwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


# 用户信息修改表单
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['nickname', 'gender', 'email', 'phone', 'qq', 'birthday','description']


# 用户密码修改表单
class ChangePwdForm(forms.Form):
    email = forms.EmailField(required=True)
    password_old = forms.CharField(required=True, min_length=6, error_messages={'required': '旧密码不能为空.', 'min_length': '旧密码不能小于6个字符.'})
    password1 = forms.CharField(required=True, min_length=6, error_messages={'required': '新密码不能为空.', 'min_length': '新密码不能小于6个字符.'})
    password2 = forms.CharField(required=True, min_length=6, error_messages={'required': '确认密码不能为空.', 'min_length': '确认密码不能小于6个字符.'})


# 上传图片表单
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserInfo  # 说明要引用的model是那个
        fields = ['image']  # 说明要使用的字段有那个
