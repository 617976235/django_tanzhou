from django.contrib import admin
from course.models import CourseClass, CourseSort, Course, Lesson, Teacher, Buy


# Register your models here.


@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_filter = ['name']


@admin.register(CourseSort)
class CourseSortAdmin(admin.ModelAdmin):
    list_display = ['classes', 'name']
    search_fields = ['classes', 'name']
    list_filter = ['classes']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['sort', 'name', 'price', 'learn_time', 'buy_nums', 'image', 'describe', 'click_nums']
    search_fields = ['name', 'price', 'learn_time', 'describe']
    list_filter = ['sort']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['lesson_course', 'name', 'lesson_time']
    search_fields = ['lesson_course', 'name', 'lesson_time']
    list_filter = ['lesson_course']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['teacher_course', 'teacher_name', 'teacher_des', 'teacher_image']
    search_fields = ['teacher_course', 'teacher_name', 'teacher_image']
    list_filter = ['teacher_course', 'teacher_name']


@admin.register(Buy)
class BuyAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['course']
