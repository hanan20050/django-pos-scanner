from datetime import timezone
from random import choices

from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    date_created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} {'(Inactive)' if not self.is_active else ''}"

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def __str__(self):
        return f"{self.name} {'(Inactive)' if not self.is_active else ''}"

class Employee(models.Model):
    ROLE_CHOICES = (
    ('Sales Agent', 'Sales Agent'),
    ('Credit Officer', 'Credit Officer'),
    ('Manager', 'Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, default='Sales Agent')
    email = models.EmailField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='media/', null=True, blank=True)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}{'' if self.is_active else ' (Inactive)'}"

    def save(self, *args, **kwargs):
        if not self.is_active and self.user.is_active:
            self.user.is_active = False
            self.user.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

class SalesAgent(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_commission_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Sales Agent: {self.employee.name}"

class CreditOfficer(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    approval_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    security_level = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Credit Officer: {self.employee.name} (Level {self.security_level})"

class Supplier(models.Model):
    OPTION = (
    ('Renewed', 'Renewed'),
    ('Opted Out', 'Opted Out'),
    ('Active', 'Active'),
    ('Expired', 'Expired')
    )

    name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    contract_expiration = models.DateField()
    contract_start = models.DateField(auto_now_add=True)
    status = models.CharField(choices=OPTION, max_length=100, default='Active')
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()

    @property
    def contract_status(self):
        today = timezone.now().date()

        if today > self.contract_expiration:
            return 'Expired'
        else:
            return self.status

    @property
    def contract_period(self):
        if not self.contract_start or not self.contract_expiration:
            return 'N/A'

        start = self.contract_start.year
        end = self.contract_expiration.year

        if start == end:
            return f"{start}"
        return f"{start} - {end}"


    def __str__(self):
        return f"{self.name} {'(Archived)' if not self.is_active else ''}"

class Product(models.Model):
    CATEGORIES = (
    ('Laptop', 'Laptop'),
    ('Android', 'Android'),
    ('iPhone', 'iPhone'),
    ('Printer', 'Printer')
    )

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=CATEGORIES, default='Laptop')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    barcode = models.CharField(max_length=100, unique=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock_level = models.PositiveIntegerField(default=3)
    image = models.ImageField(upload_to='media/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} | {self.barcode}"

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

class BranchInventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.branch} | {self.product} | {self.quantity}"

class Order(models.Model):
    ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
    )

    PAYMENT_METHOD = (
    ('CASH', 'CASH'),
    ('INSTALLMENT', 'INSTALLMENT'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'is_active': True})
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=100, default='Pending')
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=100)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.id} | {self.branch.name}"

    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, limit_choices_to={'is_active': True})
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} | {self.product.product_name}"

    @property
    def line_total(self):
        # return self.quantity * self.order.total_amount
        return self.quantity * self.unit_price

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, limit_choices_to={'is_active': True})
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    payment_type = models.CharField(max_length=100, choices=Order.PAYMENT_METHOD)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

class CashPayment(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    cash_received = models.DecimalField(max_digits=10, decimal_places=2)
    change_given = models.DecimalField(max_digits=10, decimal_places=2)

class InstallmentPlan(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    credit_officer = models.ForeignKey(CreditOfficer, on_delete=models.SET_NULL, null=True, blank=True)
    term_months = models.IntegerField()
    monthly_due = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2)
    next_due_date = models.DateField()
    payment_status = models.CharField(max_length=100, choices=Order.ORDER_STATUS)

class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='invoice', limit_choices_to={'is_active': True})
    or_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    issued_by = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return f"Invoice {self.or_number}"
