from django import forms
import django_filters
from .models import *

class InventoryFilter(django_filters.FilterSet):
    product__product_name = django_filters.CharFilter(field_name='product__product_name', lookup_expr='icontains', label='Product Name', widget=forms.TextInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none',
            'placeholder': 'Search product name...'
        }))


    product__barcode = django_filters.CharFilter(field_name='product__barcode', lookup_expr='icontains', label='Barcode',         widget=forms.TextInput(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none',
            'placeholder': 'Search barcode...'
        }))

    branch = django_filters.ModelChoiceFilter(
        queryset=Branch.objects.all(),
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white',
        })
    )

    product = django_filters.ModelChoiceFilter(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white'
        })
    )

    class Meta:
        model = BranchInventory
        fields = ['branch','product']