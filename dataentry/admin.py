from django.contrib import admin
from . models import Student
from . models import Customer

# Register your models here.
admin.site.register(Student)
admin.site.register(Customer)
