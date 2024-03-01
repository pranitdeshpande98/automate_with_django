from django.contrib import admin
from . models import Student
from . models import Customer, Employee

# Register your models here.
admin.site.register(Student)
admin.site.register(Customer)
admin.site.register(Employee)
