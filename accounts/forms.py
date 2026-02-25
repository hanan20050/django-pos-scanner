from django.forms import ModelForm
from django import forms
from .models import Employee

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'phone', 'profile_pic']
        exclude = ['user']


class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'name',
            'email',
            'phone',
            'branch',
            'role',
            'profile_pic',
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }

