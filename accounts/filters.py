import django_filters
from .models import *

class InventoryFilter(django_filters.FilterSet):
    class Meta:
        model = BranchInventory
        fields = '__all__'