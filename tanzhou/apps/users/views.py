from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from users.forms import LoginForm, RegisterForm
from users.models import UserInfo, EmailVerify
from utils.email_send import send_register_email


# Create your views here.


# 扩展用户名验证(添加qq验证)
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 首页
class IndexView(View):
    def get(self, request):
        return render(request, 'index.htm')


# 登录
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    login_message = '用户未激活.'
                    return render(request, 'login.html', locals())
            else:
                login_message = '用户名或密码错误.'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())


# 退出
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'index.htm')


# 注册
class RegisterView(View):
    def get(self, request):
        # 显示验证码
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        # 表单验证
        if register_form.is_valid():
            # 验证用户名(邮箱)是否已经存在
            if UserInfo.objects.filter(email=email):
                register_message = '用户已经存在.'
                return render(request, 'register.html', locals())
            # 保存用户信息
            user_info = UserInfo()
            user_info.username = email
            user_info.email = email
            user_info.is_active = False
            user_info.password = make_password(password)
            user_info.save()
            # 发送邮件
            send_register_email(email, 'register')
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'register.html', locals())


# 激活
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerify.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserInfo.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'success_activate.html')
        else:
            return render(request, 'register.html')

