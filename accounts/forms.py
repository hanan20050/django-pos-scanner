from django.forms import ModelForm
from django import forms
from .models import Employee

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        exclude = ['user']