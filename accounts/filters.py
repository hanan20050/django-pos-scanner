import django_filters
from .models import *

class InventoryFilter(django_filters.FilterSet):
    product__product_name = django_filters.CharFilter(field_name='product__product_name', lookup_expr='icontains', label='Product Name')
    product__barcode = django_filters.CharFilter(field_name='product__barcode', lookup_expr='icontains', label='Barcode')

    class Meta:
        model = BranchInventory
        fields = ['branch','product']