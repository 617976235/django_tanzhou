"""tanzhou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve

from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, \
    ResetPwdView
from tanzhou.settings import MEDIA_ROOT

urlpatterns = [
    # 后台登录
    url(r'^admin/', admin.site.urls),
    # 主页
    url(r'^index/$', IndexView.as_view(), name='index'),
    # 用户登录
    url(r'^login/$', LoginView.as_view(), name='login'),
    # 注销用户登录
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    # 图形验证码
    url(r'^captcha/', include('captcha.urls')),
    # 注册用户
    url(r'^register/$', RegisterView.as_view(), name='register'),
    # 激活用户
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active'),
    # 忘记密码的用户信息收集
    url(r'^forget_pwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    # 找回密码
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset'),
    # 找回密码-重置密码
    url(r'^reset_pwd/$', ResetPwdView.as_view(), name='reset_pwd'),
    # 关于用户-个人信息
    url(r'^i/', include('users.urls', namespace='i')),
    # 关于课程-课程信息
    url(r'^course/', include('course.urls', namespace='course')),
    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
