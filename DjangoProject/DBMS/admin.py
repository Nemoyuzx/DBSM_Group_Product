from django.contrib import admin
from .models import (
    Person, Student, Staff, Address, Institution, Department, 
    Course, Program, Term, RewardPunish, InstructorRole, AdminRole
)

# 注册核心模型
admin.site.register(Person)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Address)
admin.site.register(Institution)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Program)
admin.site.register(Term)
admin.site.register(RewardPunish)
admin.site.register(InstructorRole)
admin.site.register(AdminRole)
