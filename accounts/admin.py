from itertools import count

from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import items_for_result
from django.template.context_processors import request

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
    list_display = ('name', 'phone_number', 'address', 'is_active')
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ['restore_branch', 'archive_branch']

    @admin.action(description='Restore selected branch')
    def restore_branch(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully restored {count} branch.")

    @admin.action(description='Archive selected branches')
    def archive_branch(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Successfully archived {count} branches.")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'branch', 'hire_date', 'is_active')
    list_filter = ('role', 'branch', 'is_active')
    search_fields = ('name',)
    ordering = ('-is_active', 'name')

    actions = ['archive_employee','restore_employee']

    @admin.action(description='Restore selected employee')
    def restore_employee(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully restored {count} employee.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    @admin.action(description='Archive selected employee')
    def archive_employee(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"Successfully archived {count} employee.")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'address', 'date_created', 'is_active')
    search_fields = ('name', 'phone', 'email')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order__is_active=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product_name', 'category', 'base_price', 'barcode', 'is_active')
    search_fields = ('product_name', 'barcode')
    list_filter = ('is_active', 'supplier', 'category',)
    list_select_related = ('supplier',)
    ordering = ('category', 'product_name')

    actions = ['archive_products','restore_product']

    @admin.action(description='Restore selected product')
    def restore_product(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully restored {count} products.")

    @admin.action(description='Archive selected products')
    def archive_products(self, request, queryset):
        for product in queryset:
            product.soft_delete()
        self.message_user(request, f"Successfully archived {queryset.count()} products.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(BranchInventory)
class BranchInventoryAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'product__category', 'quantity', 'get_is_active')
    list_filter = ('branch', 'product', 'product__category')

    @admin.display(description='Product Active')
    def get_is_active(self, obj):
        return obj.product.is_active

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(
            product__is_active=True,
            branch__is_active=True
        )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'employee', 'branch', 'order_date', 'total_amount', 'order_status', 'payment_method', 'is_active')
    list_filter = ('is_active', 'order_status', 'branch', 'payment_method')
    search_fields = ('customer__name', 'id')

    actions = ['archive_orders','restore_orders']

    @admin.action(description='Archive selected order')
    def archive_orders(self, request, queryset):
        count = 0
        for order in queryset:
            order.soft_delete()
            count += 1
        self.message_user(request, f"Successfully archive {count} orders.")

    @admin.action(description='Restore selected orders')
    def restore_orders(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"Sucsessfully restored {updated} orders.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('or_number', 'invoice_date', 'vat_amount', 'grand_total', 'issued_by', 'order__customer')
    list_filter = ('or_number', 'order__customer')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order__is_active=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

@admin.register(SalesAgent)
class SalesAgentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'commission_rate', 'total_commission_earned', 'total_sales', 'get_branch', 'get_status')
    list_filter = ('employee__branch', 'employee__is_active')
    list_select_related = ('employee__branch',)

    def get_branch(self, obj):
        return obj.employee.branch
    get_branch.short_description = 'Branch'
    get_branch.admin_order_field = 'employee__branch'

    actions = ['archive_officer', 'restore_officer']

    @admin.display(description='Officer Name', ordering='employee__name')
    def get_name(self, obj):
        return obj.employee.name

    @admin.display(description='Status', boolean=True)
    def get_status(self, obj):
        return obj.employee.is_active

    @admin.display(description='Total Applications')
    def get_plans_count(self, obj):
        return obj.installmentplan_set.count()

    @admin.action(description='Archive selected officer')
    def archive_officer(self, request, queryset):
        count = 0
        for officer in queryset:
            officer.employee.is_active = False
            officer.employee.save()
            count += 1
        self.message_user(request, f"Successfully archived {count} officers.")

    @admin.action(description='Restore selected officer')
    def restore_officer(self, request, queryset):
        count = 0
        for officer in queryset:
            officer.employee.is_active = True
            officer.employee.save()
            count += 1
        self.message_user(request, f"Successfully restored {count} officers.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(CreditOfficer)
class CreditOfficerAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'approval_limit', 'security_level', 'get_plans_count', 'get_status')
    search_fields = ('employee__name',)
    list_filter = ('employee__is_active',)

    inlines = [InstallmentPlanInline]

    actions = ['archive_officer', 'restore_officer']

    @admin.display(description='Officer Name', ordering='employee__name')
    def get_name(self, obj):
        return obj.employee.name

    @admin.display(description='Status', boolean=True)
    def get_status(self, obj):
        return obj.employee.is_active

    @admin.display(description='Total Applications')
    def get_plans_count(self, obj):
        return obj.installmentplan_set.count()

    @admin.action(description='Archive selected officer')
    def archive_officer(self, request, queryset):
        count = 0
        for officer in queryset:
            officer.employee.is_active = False
            officer.employee.save()
            count += 1
        self.message_user(request, f"Successfully archived {count} officers.")

    @admin.action(description='Restore selected officer')
    def restore_officer(self, request, queryset):
        count = 0
        for officer in queryset:
            officer.employee.is_active = True
            officer.employee.save()
            count += 1
        self.message_user(request, f"Successfully restored {count} officers.")


    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions is not None and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'unit_price')
    list_filter = ('order__branch',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order__is_active=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount_paid', 'date_paid', 'payment_type')
    list_filter = ('payment_type', 'order__branch')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(order__is_active=True)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

class get_active_branch(admin.SimpleListFilter):
    title = 'Active Branch'
    parameter_name = 'branch'
    def lookups(self, request, model_admin):
        return [(branch.id, branch.name) for branch in Branch.objects.filter(is_active=True)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(payment__order__branch_id=self.value())
        else:
            return queryset

@admin.register(CashPayment)
class CashPaymentAdmin(admin.ModelAdmin):
    list_display = ('payment', 'get_employee', 'get_branch', 'get_customer_name', 'get_product', 'get_total_amount', 'cash_received', 'change_given', 'get_date')
    list_filter = (get_active_branch,)

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

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(payment__order__is_active=True)

@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('payment', 'term_months', 'monthly_due', 'remaining_balance', 'next_due_date', 'payment_status')
    list_filter = ('payment_status',)

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.filter(payment__order__is_active=True)

    def get_queryset(self, request):
        # qs = super().get_queryset(request)
        return super().get_queryset(request).filter(payment__order__is_active=True)

    def has_add_permission(self, request):
        return False


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'phone', 'contract_start', 'contract_period', 'contract_status', 'contract_expiration', 'is_active')
    search_fields = ('name', 'contact_person')
    list_filter = ('status', 'is_active')

    actions = ['archive_products','restore_product']

    @admin.action(description='Restore selected product')
    def restore_product(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"Successfully restored {count} products.")

    @admin.action(description='Archive selected products')
    def archive_products(self, request, queryset):
        for product in queryset:
            product.soft_delete()
        self.message_user(request, f"Successfully archived {queryset.count()} products.")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if actions and 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # @admin.display(description='Status', boolean=True)
    # def get_status(self, obj):
    #     return obj.is_active


from django.contrib import admin
from .models import WarrantyClaims, ReplacementRecord


@admin.register(WarrantyClaims)
class WarrantyClaimsAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_item', 'claim_type', 'status', 'cost_impact', 'handled_by', 'date_filed')

    list_filter = ('claim_type', 'status', 'handled_by')

    search_fields = ('fault_serial', 'order_item__product__product_name', 'issue_description')


    readonly_fields = ('date_filed',)

    def has_add_permission(self, request):
        return False


@admin.register(ReplacementRecord)
class ReplacementRecordAdmin(admin.ModelAdmin):
    list_display = ('warranty_claims', 'old_serial', 'new_serial', 'replacement_date')

    def has_add_permission(self, request):
        return False

@admin.register(DefectiveInventory)
class DefectiveInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'branch', 'faulty_serial', 'reason', 'date_received', 'is_disposed')
    list_filter = ('branch', 'faulty_serial')

    def has_add_permission(self, request):
        return False

