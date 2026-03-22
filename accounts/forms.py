from django.forms import ModelForm
from django import forms
from .models import Employee, Product, InstallmentPlan, Payment

class InstallmentPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_paid']
        widgets = {
            'amount_paid': forms.NumberInput(attrs={
                'class': 'form-control', 'step': '0.01'
            }),
        }

class ProductForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        empty_label='--Select Product--',
        widget=forms.Select(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'id': 'product_select',
        })
    )

    class Meta:
        model = Product
        fields = ['product']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['email', 'phone', 'profile_pic']
        exclude = ['user']


class EmployeeAdminForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-600 focus:ring-0 font-semibold',
            'placeholder': 'Create a login username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-600 focus:ring-0 font-semibold',
            'placeholder': 'Set a temporary password'
        })
    )

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

