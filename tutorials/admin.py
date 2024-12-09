from django.contrib import admin
from .models.tutor_model import Tutor
from .models.student_model import Student
from .models.admin_model import Admin

admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Admin)
