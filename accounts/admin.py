from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import items_for_result

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
    list_display = ('name', 'phone_number', 'address')
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
    list_display = ('supplier', 'product_name', 'category', 'base_price', 'barcode', 'is_active')
    search_fields = ('product_name', 'barcode')
    list_filter = ('is_active', 'supplier', 'category',)
    list_select_related = ('supplier',)
    ordering = ('category', 'product_name')

    actions = ['restore_product']

    @admin.action(description='Restore selected product')
    def restore_product(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully restored {count} products.")


@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'quantity', 'get_is_active')
    list_filter = ('branch', 'product')

    @admin.display(description='Product Active')
    def get_is_active(self, obj):
        return obj.product.is_active

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(product__is_active=True)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'employee', 'branch', 'order_date', 'total_amount', 'order_status', 'payment_method', 'is_active')
    list_filter = ('is_active', 'order_status', 'branch', 'payment_method')
    search_fields = ('customer__name', 'id')

    actions = ['restore_orders']

    @admin.action(description='Restore selected orders')
    def restore_orders(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Sucsessfully restored {updated} orders.")

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('or_number', 'invoice_date', 'vat_amount', 'grand_total', 'issued_by', 'order__customer')
    list_filter = ('or_number', 'order__customer')

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'commission_rate', 'total_commission_earned', 'total_sales', 'get_branch')
    list_filter = ('employee__branch',)
    list_select_related = ('employee__branch',)

    def get_branch(self, obj):
        return obj.employee.branch
    get_branch.short_description = 'Branch'
    get_branch.admin_order_field = 'employee__branch'

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
    list_filter = ('order__branch',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount_paid', 'date_paid', 'payment_type')
    list_filter = ('payment_type', 'order__branch')

@admin.register(CashPayment)
class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'get_employee', 'get_branch', 'get_customer_name', 'get_product', 'get_total_amount', 'cash_received', 'change_given', 'get_date')
    # list_filter = ('payment',)

    @admin.display(ordering='payment__order__total_amount', description='Total Amount')
    def get_total_amount(self, obj):
        return f"₱{obj.payment.order.total_amount}"

    @admin.display(description='Customer Name')
    def get_customer_name(self, obj):
        customer = obj.payment.order.customer
        return customer.name if customer else "No customer found"

    @admin.display(description='Branch')
    def get_branch(self, obj):
        branch = obj.payment.order.branch
        return branch.name if branch else "No branch found"

    @admin.display(description='Employee')
    def get_employee(self, obj):
        employees = obj.payment.order.employee
        return employees.name if employees else "No employee found"

    @admin.display(description='Date')
    def get_date(self, obj):
        order_date = obj.payment.order.order_date

        if order_date:
            return order_date.strftime('%B %d, %Y')

        return "No date found"


    @admin.display(description='Product Name')
    def get_product(self, obj):
        items = obj.payment.order.orderitem_set.select_related('product').all()

        if items.exists():
            return ", ".join([item.product.product_name for item in items])
        return "No products"

@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('payment', 'term_months', 'monthly_due', 'remaining_balance', 'next_due_date', 'payment_status')
    list_filter = ('payment_status',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'contract_start', 'contract_period', 'contract_status', 'contract_expiration')
    search_fields = ('name', 'contact_person')
    list_filter = ('status',)

