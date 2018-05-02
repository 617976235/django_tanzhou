from django.contrib import admin
from users.models import UserInfo, EmailVerify, SlideShow

# Register your models here.


@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'phone', 'qq', 'nickname', 'birthday', 'gender', 'is_superuser', 'is_active',
                    'is_staff', 'last_login']
    search_fields = ['username', 'email', 'phone', 'qq', 'nickname']
    list_filter = ['gender', 'is_superuser', 'is_active', 'is_staff']


@admin.register(EmailVerify)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ['email', 'code', 'send_type', 'send_time']
    search_fields = ['email', 'code', 'send_type', 'send_time']
    list_filter = ['send_type']


@admin.register(SlideShow)
class SlideShowAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'url', 'index', 'add_time']
    search_fields = ['name', 'url', 'index', 'add_time']

