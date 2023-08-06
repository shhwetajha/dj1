from django.contrib import admin
from django.contrib.auth.models import User
from ems.models import Student

# Register your models here.
@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    list_display=['name','age','rollno']

