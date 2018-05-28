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
from django.conf.urls import url
from users.views import UserInfoView, ChangePwdView, UploadImageView, UserOrderView, UserWorkView, UserCourseView


urlpatterns = [
    # 用户信息
    url(r'info/$', UserInfoView.as_view(), name='info'),
    # 修改密码
    url(r'change_pwd/$', ChangePwdView.as_view(), name='change_pwd'),
    # 用户头像上传
    url(r'image_upload/$', UploadImageView.as_view(), name="image_upload"),
    # 我的订单
    url(r'order/$', UserOrderView.as_view(), name="order"),
    # 我的作业
    url(r'homework/$', UserWorkView.as_view(), name="homework"),
    # 我的课程
    url(r'course/$', UserCourseView.as_view(), name="course"),
]


