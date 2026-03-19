from django.contrib import admin
from . models import *

# Register your models here.

class InstallmentPlanInline(admin.TabularInline):
    model = InstallmentPlan
    extra = 0
    readonly_fields = ('payment', 'term_months', 'monthly_due', 'remaining_balance', 'next_due_date', 'payment_status')
    can_delete = False
    show_change_link = True

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'branch', 'hire_date')
    list_filter = ('role', 'branch')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'date_created')
    search_fields = ('name', 'phone', 'email')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product_name', 'category', 'base_price', 'barcode')
    search_fields = ('product_name', 'barcode')


@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'quantity')
    list_filter = ('branch',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'employee', 'branch', 'order_date', 'total_amount', 'order_status', 'payment_method')
    list_filter = ('order_status', 'branch', 'payment_method')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('or_number', 'invoice_date', 'vat_amount', 'grand_total', 'issued_by')
    list_filter = ('or_number',)

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'commission_rate', 'total_commission_earned', 'total_sales',)
    list_filter = ('employee',)

@admin.register(CreditOfficer)
class CreditOfficerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'approval_limit', 'security_level', 'get_plans_count')
    search_fields = ('employee__name',)

    inlines = [InstallmentPlanInline]

    @admin.display(description='Officer Name', ordering='employee__name')
    def get_name(self, obj):
        return obj.employee.name

    @admin.display(description='Total Applications')
    def get_plans_count(self, obj):
        return obj.installmentplan_set.count()

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price')
    list_filter = ('order',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount_paid', 'date_paid', 'payment_type')
    list_filter = ('order',)

@admin.register(CashPayment)
class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'cash_received', 'change_given')
    list_filter = ('payment',)

@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('payment', 'term_months', 'monthly_due', 'remaining_balance', 'next_due_date', 'payment_status')
    list_filter = ('payment',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'contract_start', 'contract_period', 'contract_status', 'contract_expiration')
    search_fields = ('name', 'contact_person')
    list_filter = ('status',)

