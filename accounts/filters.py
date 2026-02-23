from django import forms
import django_filters
from .models import *
from django.db.models import F

class InventoryFilter(django_filters.FilterSet):
    STOCK_CHOICES = (
    ('low', 'Low Stocks'),
    ('out', 'Out of stocks'),
    ('in stock', 'In stock'),
    )

    stock_status = django_filters.ChoiceFilter(choices=STOCK_CHOICES, method='filter_stock_status', label='Stock Status', widget=forms.Select(attrs={'class': 'px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none bg-white',}))

    def filter_stock_status(self, queryset, name, value):
        if value == 'low':
            # Returns items where quantity is > 0 but <= min_stock_level
            return queryset.filter(quantity__gt=0, quantity__lte=F('product__min_stock_level'))
        elif value == 'out':
            # Returns items where quantity is 0 or less
            return queryset.filter(quantity__lte=0)
        elif value == 'healthy':
            # Returns items where quantity is strictly greater than min_stock_level
            return queryset.filter(quantity__gt=F('product__min_stock_level'))
        return queryset


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