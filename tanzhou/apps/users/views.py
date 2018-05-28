from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

from users.forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UserInfoForm, ChangePwdForm, \
    UploadImageForm
from users.models import UserInfo, EmailVerify
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin


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
        return render(request, 'index.html')


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
        return render(request, 'index.html')


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


# 忘记密码的用户信息收集
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        email = request.POST.get('email')
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            if UserInfo.objects.filter(email=email):
                send_register_email(email, 'forget')
                return render(request, 'send_success.html', locals())
            else:
                forget_message = '用户不存在.'
                return render(request, 'forgetpwd.html', locals())
        else:
            return render(request, 'forgetpwd.html', locals())


# 找回密码页面
class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerify.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', locals())


# 找回密码-重置密码
class ResetPwdView(View):
    def post(self, request):
        email = request.POST.get('email')
        print(email)
        reset_form = ResetPwdForm(request.POST)
        if reset_form.is_valid():
            password = reset_form.cleaned_data['password']
            password2 = reset_form.cleaned_data['password2']
            print(password2)
            if password == password2:
                user = UserInfo.objects.get(email=email)
                user.password = make_password(password2)
                user.save()
                # return HttpResponseRedirect(reverse('login'))
                return render(request, 'reset_success.html')
            else:
                reset_message = '两次输入的密码不一致.'
                return render(request, 'password_reset.html', locals())
        else:
            return render(request, 'password_reset.html', locals())


# 用户信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_info/my_info.html', locals())

    def post(self, request):
        user_form = UserInfoForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse("i:info"))
        else:
            return render(request, 'user_info/my_info.html', locals())


# 用户密码-修改密码
class ChangePwdView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.user.email
        return render(request, 'user_info/my_password.html', locals())

    def post(self, request):
        change_form = ChangePwdForm(request.POST)
        email = request.user.email
        # 验证前端的数据
        if change_form.is_valid():
            password_old = request.POST.get("password_old", "")
            # email = request.POST.get("email", "")
            user = authenticate(username=email, password=password_old)
            if user is not None:
                pwd1 = request.POST.get("password1", "")
                pwd2 = request.POST.get("password2", "")
                if pwd1 == pwd2:
                    user = UserInfo.objects.get(email=email)
                    user.password = make_password(pwd2)
                    user.save()
                    return render(request, 'reset_success.html')
                return render(request, "user_info/my_password.html", {"email": email, "msg": u"密码不一致."})
            return render(request, "user_info/my_password.html", {"email": email, "msg_old": u"旧密码不对."})
        return render(request, 'user_info/my_password.html', {'change_form': change_form, 'email': email})


# 用户订单
class UserOrderView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_info/my_order.html', {})

    def post(self, request):
        pass


# 用户作业
class UserWorkView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_info/my_homework.html', {})

    def post(self, request):
        pass


# 用户课程
class UserCourseView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_info/my_course.html', {})

    def post(self, request):
        pass


# 用户头像-修改头像
class UploadImageView(LoginRequiredMixin, View):
    # def post(self, request):
    #     # 把前段传入的数据保存    直接实例化,实例化直接保存
    #     image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
    #     print(dir(image_form))
    #     if image_form.is_valid():
    #         image_form.save()
    #         return HttpResponseRedirect(reverse("i:info"))
    #     else:
    #         return render(request, 'my_info.html')

    # 常规方式
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponseRedirect(reverse("i:info"))
        else:
            return render(request, 'user_info/my_info.html')
