from contextlib import nullcontext
from functools import total_ordering
from http.client import responses
from sys import is_stack_trampoline_active, exception
from xmlrpc.client import WRAPPERS

from django.contrib.admin.templatetags.admin_list import items_for_result, paginator_number
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import csrf_token
from django.utils.text import phone2numeric, compress_string

from .decorators import unauthenticated_user
from .models import Product, Employee, Branch, BranchInventory, Customer, Order, OrderItem, Payment, CashPayment, \
    CreditOfficer, InstallmentPlan, Invoice, WarrantyClaims, DefectiveInventory
from .filters import InventoryFilter, salesFilter, installmentFilter
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import EmployeeForm, EmployeeAdminForm, ProductForm, InstallmentPaymentForm
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db import transaction

from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from django.db.models import Sum, F, Expression, ExpressionWrapper, Count, Q
from django.db import models

import re
from decimal import Decimal

from django.http import JsonResponse
import json
import uuid




# Create your views here.

class InventoryUpdateView(UpdateView):
    model = BranchInventory
    fields = ['quantity']
    template_name = 'accounts/inventory_update.html'
    success_url = reverse_lazy('branch_inventory')

class salesUpdateView(UpdateView):
    model = Order
    fields = ['employee', 'order_status']
    template_name = 'components/sales_edit.html'
    success_url = reverse_lazy('sales_display')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        print(f"DEBUG: Updating order for: {obj.customer}")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['invoice'] = Invoice.objects.filter(order=self.object).first()
        return context

@login_required(login_url='login')
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    order.soft_delete()

    messages.success(request, f"Order #{order.id} has been archived")

    return redirect('sales_display')

@login_required(login_url='login')
def admin_reports(request):

    now = timezone.now()

    current_month_transactions = Order.objects.filter(
        order_date__year=now.year,
        order_date__month=now.month,
        employee__is_active=True,
        branch__is_active = True,
        is_active = True
    )

    active_order_ids = current_month_transactions.values_list('id', flat=True)

    stats = OrderItem.objects.filter(
        order_id__in=active_order_ids,
        product__is_active=True  # Ensure we only count active products
    ).aggregate(
        total_revenue=Sum(F('unit_price') * F('quantity')),
        total_cost=Sum(F('quantity') * F('cost_price')),
        total_count=Count('order_id', distinct=True)
    )

    # orders_stats = current_month_transactions.filter(
    #     is_active=True  # Use the Order's own status
    # ).aggregate(
    #     total_revenue=Sum('total_amount'),
    #     total_count=Count('id', distinct=True)
    # )
    #
    # cost_stats = OrderItem.objects.filter(
    #     order__in=current_month_transactions,
    #     product__is_active=True
    # ).aggregate(
    #     total_cost=Sum(F('quantity') * F('cost_price'))
    # )


    or_balance = InstallmentPlan.objects.filter(
        payment_status__in=['Pending', 'Cancelled']
    ).aggregate(total_owed=Sum('remaining_balance'))['total_owed'] or Decimal('0.00')

    outstanding_balance = or_balance.quantize(Decimal('0.00'))

    payments = OrderItem.objects.filter(
        order_id__in=active_order_ids,
        product__is_active=True
    ).aggregate(
        cash=Sum(
            F('unit_price') * F('quantity'),
            filter=Q(order__payment_method='CASH')
        ),
        installment=Sum(
            F('unit_price') * F('quantity'),
            filter=Q(order__payment_method='INSTALLMENT')
        )
    )

    branch_query = Order.objects.filter(
        id__in=active_order_ids
    ).values('branch__name').annotate(
        total=Sum('total_amount')
    ).order_by('-total')


    branch_names = []
    branch_totals = []

    if branch_query.exists():
        for data_row in branch_query:
            name = data_row['branch__name'] if data_row['branch__name'] else "Main Store"
            amount = float(data_row['total']) if data_row['total'] else 0.0

            branch_names.append(name)
            branch_totals.append(amount)

    employee_sales = Order.objects.filter(
        id__in=active_order_ids
    ).values('employee__name').annotate(
        total=Sum('total_amount')
    ).order_by('-total')

    employee_names = [
        f"{item['employee__name']}" if item['employee__name'] else "System Admin"
        for item in employee_sales
    ]

    employee_totals = [float(item['total'] or 0) for item in employee_sales]

    product_sales = OrderItem.objects.filter(
        order_id__in=active_order_ids,
        product__is_active=True
    ).values('product__product_name').annotate(
        total=Sum('quantity')
    ).order_by('-total')[:5]

    product_name = [
        f"{item['product__product_name']}" if item['product__product_name'] else "Out of Stock"
        for item in product_sales
    ]

    product_totals = [float(item['total'] or 0) for item in product_sales]

    print(len(product_sales))


    gross_revenue = stats['total_revenue'] or 0
    cost = stats['total_cost'] or 0
    total_count = stats['total_count'] or 0
    total_transactions = stats['total_count'] or 0
    net_profit = gross_revenue - cost
    cash_total = payments['cash'] or 0
    installment_total = payments['installment'] or 0

    transactions = Order.objects.filter(employee__is_active=True, branch__is_active=True, is_active=True).select_related('customer', 'branch').prefetch_related('orderitem_set__product').order_by('-order_date')

    if gross_revenue > 0:
        ratio = float(outstanding_balance / gross_revenue)
    else:
        ratio = 0

    aov = gross_revenue / total_count if total_count > 0 else 0


    paginator = Paginator(transactions, 7)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'gross_revenue': gross_revenue, 'cost': cost, 'net_profit': net_profit, 'aov': aov, 'ratio': ratio, 'outstanding_balance': outstanding_balance, 'total_transactions': total_transactions, 'transactions': transactions, 'page_obj': page_obj, 'cash_total': cash_total, 'installment_total': installment_total, 'branch_names': branch_names,
    'branch_totals': branch_totals, 'employee_names': employee_names,
    'employee_totals': employee_totals, 'product_name': product_name, 'product_totals': product_totals}

    print(gross_revenue)

    return render(request, 'accounts/admin_reports.html', context)



@login_required(login_url='login')
def admin_installment(request):
    is_manager = request.user.is_superuser or hasattr(request.user, 'employee') and request.user.employee.role == 'Manager'

    installment_sales = OrderItem.objects.filter(order__payment_method='INSTALLMENT').select_related('order', 'order__customer', 'product', 'order__employee').order_by('-order__order_date', '-id')

    myFilter = installmentFilter(request.GET, queryset=installment_sales)
    filtered_items = myFilter.qs

    inst = Order.objects.filter(payment_method='INSTALLMENT').count()

    sales_result = filtered_items.aggregate(total=Sum('order__total_amount'))
    grand_total = sales_result['total'] or 0

    context = {'installment_sales': installment_sales, 'myFilter': myFilter, 'is_manager': is_manager, 'inst': inst, 'grand_total': grand_total}

    return render(request, 'accounts/admin_installment.html', context)

@login_required(login_url='login')
def manage_installment(request, pk):

    inst = get_object_or_404(InstallmentPlan, payment__order__pk=pk)

    inst.refresh_from_db()

    print(f"DEBUG: Current Balance in DB: {inst.remaining_balance}")

    payments = Payment.objects.filter(order=inst.payment.order).order_by('-date_paid')

    if request.method == 'POST':
        form = InstallmentPaymentForm(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount_paid']

            if amount > inst.remaining_balance:
                print("Payment exceeds remaining balance.")
                return render(request, 'accounts/manage_installment.html', {'inst': inst, 'form': form})

            try:
                with transaction.atomic():
                    new_payment = form.save(commit=False)
                    new_payment.order = inst.payment.order
                    new_payment.payment_type = 'INSTALLMENT'
                    new_payment.save()  # <--- IF THIS FAILS, THE WHOLE BLOCK STOPS

                    inst.remaining_balance -= amount
                    inst.next_due_date += timedelta(days=30)
                    inst.save()

                    messages.success(request, "Payment successful")
                    return redirect('manage_installment', pk=pk)
            except Exception as e:
                print(f"!!! TRANSACTION FAILED: {e}")
                messages.error(request, f"Error: {e}")
        else:
            return redirect('manage_installment', pk=inst.pk)
    else:
        form = InstallmentPaymentForm()

    payment = Payment.objects.filter(order=inst.payment.order)

    print(f"DEBUG: Looking for payments for Order ID: {inst.payment.order.id}")
    print(f"DEBUG: Found {payments.count()} payments.")

    context = {'inst': inst, 'form': form, 'payment': payment, 'payments': payments}

    return render(request, 'accounts/manage_installment.html', context)

@login_required(login_url='login')
def emp_receipt(request, pk):

    order = get_object_or_404(Order, pk=pk)
    invoice = Invoice.objects.filter(order=order).first()
    context = {'order': order, 'invoice': invoice}

    return render(request, 'accounts/emp_receipt.html', context)

@login_required(login_url='login')
def instCalculator(request):
    product_count = Product.objects.count()
    all_products = Product.objects.all()

    form = ProductForm()
    product_data = None

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            selected_product = form.cleaned_data.get('product')
            product_data = selected_product


    context = {'form':form, 'product_data':product_data, 'sales_agent': request.user.employee, 'product_count': product_count, 'all_products': all_products}

    return render(request, 'accounts/inst_calculator.html', context)


@login_required(login_url='login')
def home(request):
    return render(request, 'accounts/main.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
            # else:
            # messages.info(request, 'Username or password is incorrect.')

    # context = {}
    return render(request, 'accounts/login.html')

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def salesDisplay(request):
    is_manager = request.user.is_superuser or hasattr(request.user, 'employee') and request.user.employee.role == 'Manager'

    if is_manager:
        queryset = OrderItem.objects.filter(order__is_active=True).select_related('order', 'order__customer', 'product', 'order__employee')
    else:
        try:
            assigned_branch = request.user.employee.branch

            queryset = OrderItem.objects.filter(order__branch=assigned_branch, order__is_active=True).select_related('order', 'product')
        except Employee.DoesNotExist:
            queryset = OrderItem.objects.none

    queryset = queryset.order_by('-order__order_date')

    myFilter = salesFilter(request.GET, queryset=queryset)
    filtered_items = myFilter.qs

    inst = Order.objects.filter(payment_method='INSTALLMENT').count()
    cash_sales = Order.objects.filter(payment_method='CASH').count()
    print(f"DEBUG: Cash sales count is {cash_sales}")

    result = filtered_items.aggregate(
        total_revenue=Sum(
            ExpressionWrapper(
                F('unit_price') * F('quantity'),
                output_field=models.DecimalField()
            )
        )
    )

    grand_total = result['total_revenue'] or 0

    paginator = Paginator(filtered_items, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'myFilter': myFilter, 'is_manager': is_manager, 'sales': page_obj, 'grand_total': grand_total, 'inst': inst, 'cash_sales': cash_sales}

    return render(request, 'accounts/sales_display.html', context)

@login_required(login_url='login')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    product.soft_delete()

    messages.success(request, f"{product.product_name} has been archived globally.")
    return redirect('branch_inventory')

@login_required(login_url='login')
def branchInventory(request):
    is_manager = request.user.is_superuser or hasattr(request.user, 'employee') and request.user.employee.role == 'Manager'


    if is_manager:
        items = BranchInventory.objects.filter(product__is_active=True).select_related('branch', 'product')
        assigned_branch = 'All Branches'
    else:
        try:
            login_employee = Employee.objects.get(user=request.user)
            assigned_branch = login_employee.branch

            items = BranchInventory.objects.filter(branch=assigned_branch, product__is_active=True).select_related('product', 'product__supplier')

        except Employee.DoesNotExist:
            items = BranchInventory.objects.none()
            assigned_branch = 'None assigned'

    myFilter = InventoryFilter(request.GET, queryset=items)
    filtered_items = myFilter.qs

    paginator = Paginator(filtered_items, 8)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/branch_inventory.html', {
        'myFilter': myFilter,
        'items':page_obj,
        'assigned_branch':assigned_branch,
        'is_manager':is_manager,}
        )


def employeeProfile(request):
    sales_agent = request.user.employee
    form = EmployeeForm(instance=sales_agent)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=sales_agent)

        if form.is_valid():
            form.save()
            return redirect('employee_profile')


    context = {'form':form, 'sales_agent':sales_agent}
    return render(request, 'accounts/employee_profile.html', context)


class EmployeeList(ListView):
    model = Employee
    template_name = 'accounts/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 3

    def get_queryset(self):
        return Employee.objects.filter(is_active=True).order_by('-hire_date')



class EmployeeCreate(SuccessMessageMixin, CreateView):
    model = Employee
    form_class = EmployeeAdminForm
    success_url = reverse_lazy('employee_list')
    template_name = 'accounts/employee_form.html'
    success_message = "Employee %(name)s was created successfully!"

    def form_valid(self, form):
        custom_username = form.cleaned_data.get('username')
        custom_password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')

        if User.objects.filter(username=custom_username).exists():
            form.add_error('username', 'This username is already taken.')
            return self.form_invalid(form)


        user = User.objects.create_user(
            username=custom_username,
            email=email,
            password=custom_password
        )

        employee = form.save(commit=False)
        employee.user = user
        employee.save()

        return redirect(self.success_url)


def manageEmployee(request, pk):
    # print(f"\n\n--- DEBUG: ACCESSING PK {pk} --- \n\n")
    # raise Exception(f"I am in the manageEmployee function with PK {pk}")

    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeAdminForm(request.POST, request.FILES, instance=employee)

        if form.is_valid():
            employee = form.save(commit=False)
            user = employee.user

            user.email = form.cleaned_data.get('email')

            new_password = form.cleaned_data.get('password')
            if new_password:
                user.set_password(new_password)

            user.save()
            employee.save()

            return redirect('employee_list')

    else:
        form = EmployeeAdminForm(instance=employee)
        print(f"DEBUG: Form instance PK is {form.instance.pk}")

    context = {'employee':employee, 'form':form}
    return render(request, 'accounts/employee_form.html', context)


# @login_required(login_url='login')
# def posTerminal(request):
#     return render(request, 'accounts/pos_terminal.html')

@login_required(login_url='login')
def posTerminal(request):
    employee = get_object_or_404(Employee, user=request.user)
    branch_products = BranchInventory.objects.filter(branch=employee.branch).select_related('product')
    credit_officers = Employee.objects.filter(role='Credit Officer')

    context = {'employee':employee, 'branch_products':branch_products, 'credit_officers': credit_officers}

    return render(request, 'accounts/pos_terminal.html', context)


@login_required(login_url='login')
def scanProduct(request):
    barcode = request.GET.get('barcode')

    employee = get_object_or_404(Employee, user=request.user)

    print(f"--- SCAN DEBUG ---")
    print(f"Input Barcode: '{barcode}'")
    print(f"Branch: {employee.branch}")

    inventory_item = BranchInventory.objects.filter(
        product__barcode__iexact=barcode,
        branch=employee.branch
    ).select_related('product').first()

    if not inventory_item:
        exists_anywhere = Product.objects.filter(barcode=barcode).exists()
        print(f"Exists anywhere in system: {exists_anywhere}")
        return JsonResponse({'error': 'Product not found'}, status=404)

    return JsonResponse({
        'id': inventory_item.product.id,
        'name': inventory_item.product.product_name,
        'price': str(inventory_item.product.base_price),
        'stock': inventory_item.product.min_stock_level,
        'image': inventory_item.product.image.url,
    })

@transaction.atomic
def checkout_cash(request):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)

                cart = data.get('cart', [])
                total_amount = Decimal(str(data.get('totalAmount', 0)))
                cash_received = data.get('cashReceived')
                change_given = data.get('changeGiven')
                customer_data = data.get('customerData', {})
                payment_method = data.get('paymentMethod')

                if cash_received is None:
                    return JsonResponse({'success': False, 'message': 'Cash received amount is missing'}, status=400)

                if not cart:
                    return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)

                try:
                    employee = request.user.employee
                    branch = employee.branch
                except Exception:
                    return JsonResponse({'success': False, 'message': 'User is not an authorized employee'}, status=403)

                customer = None
                phone = customer_data.get('phone')

                if phone:
                    customer, created = Customer.objects.get_or_create(
                        phone = phone,
                        defaults={
                            'name': customer_data.get('name', 'Walk-in'),
                            'email': customer_data.get('email', ''),
                            'address': customer_data.get('address', '')
                        }
                    )

                order = Order.objects.create(
                    employee = employee,
                    branch = branch,
                    customer = customer,
                    total_amount = total_amount,
                    payment_method = payment_method,
                    order_status = Order.ORDER_STATUS[1][0]

                )

                for item in cart:
                    product = Product.objects.get(id=item['id'])
                    OrderItem.objects.create(
                        order = order,
                        product = product,
                        quantity = item['qty'],
                        unit_price = Decimal(str(item['price'])),
                        cost_price = product.cost_price
                    )

                    try:
                        inventory = BranchInventory.objects.get(branch=branch, product=product)
                    except BranchInventory.DoesNotExist:
                        raise ValueError(f"Product {product.product_name} is not registered at this branch.")

                    if inventory.quantity < int(item['qty']): raise ValueError("Out of Stock")

                    inventory.quantity -= int(item['qty'])

                    inventory.save()

                payment = Payment.objects.create(
                    order = order,
                    amount_paid = cash_received,
                    payment_type = payment_method,
                    date_paid = order.order_date
                )

                CashPayment.objects.create(
                    payment = payment,
                    cash_received = cash_received,
                    change_given = change_given,
                )

                Invoice.objects.create(
                    order=order,
                    or_number=f"OR-{uuid.uuid4().hex[:8].upper()}",
                    vat_amount=order.total_amount * Decimal('0.12'),
                    grand_total=order.total_amount,
                    issued_by=order.employee,
                    invoice_date = order.order_date
                )

                try:
                    agent_profile = order.employee.salesagent
                    agent_profile.total_sales += order.total_amount
                    commission_for_this_order = order.total_amount * agent_profile.commission_rate
                    agent_profile.total_commission_earned += commission_for_this_order
                    agent_profile.save()
                except Exception:
                    pass


                return JsonResponse({'success': True, 'order_id': order.id})

            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)}, status=400)

        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)



def clean_currency(value):
    if isinstance(value, (int, float, Decimal)):
        return Decimal(value)
    clean_val = re.sub(r'[^\d.]', '', str(value))
    return Decimal(clean_val) if clean_val else Decimal('0.00')



@csrf_exempt
@transaction.atomic
def installment_checkout(request):
    print(f"DEBUG: Request reached view. CSRF Middleware Token in request: {request.headers.get('X-CSRFToken')}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cart = data.get('cart', [])
            total_amount = data.get('totalAmount')
            installment_total = data.get('installmentTotal')
            installment_data = data.get('installmentData')
            payment_method = data.get('paymentMethod')

            if installment_data.get('downpayment') is None:
                return JsonResponse({'success': False, 'message': 'Downpayment received amount is missing'}, status=400)

            if not cart:
                return JsonResponse({'success': False, 'message': 'Cart is empty'}, status=400)

            try:
                sales_agent = request.user.employee.salesagent
                branch = request.user.employee.branch
            except Exception:
                return JsonResponse({'success': False, 'message': 'You must be a Sales Agent to process orders'},
                                    status=403)

            try:
                officer_id = installment_data.get('creditOfficerId')
                print(f"DEBUG: Attempting to find Credit Officer with ID: '{officer_id}'")
                credit_officer = CreditOfficer.objects.get(employee_id=officer_id)
            except CreditOfficer.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'test'},
                                    status=400)

            customer = None
            phone = installment_data.get('phone')
            payment = clean_currency(installment_data.get('downpayment'))
            term_months = installment_data.get('term')
            monthly_due = clean_currency(installment_data.get('monthlyPayment'))
            remaining_balance = clean_currency(installment_data.get('balanceToFinance'))

            if phone:
                customer, created = Customer.objects.get_or_create(
                    phone=phone,
                    defaults={
                        'name': installment_data.get('name', 'Walk-in'),
                        'email': installment_data.get('email', ''),
                        'address': installment_data.get('address', '')
                    }
                )

            order = Order.objects.create(
                employee = sales_agent.employee,
                branch = branch,
                customer = customer,
                total_amount = total_amount,
                payment_method = payment_method,
                order_status = Order.ORDER_STATUS[0][0]
            )

            for item in cart:
                product = Product.objects.get(id=item['id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['qty'],
                    unit_price=item['price']
                )

                try:
                    inventory = BranchInventory.objects.get(branch=branch, product=product)
                except BranchInventory.DoesNotExist:
                    raise ValueError(f"Product {product.product_name} is not registered at this branch.")

                if inventory.quantity < int(item['qty']): raise ValueError("Out of Stock")

                inventory.quantity -= int(item['qty'])

                inventory.save()

            payment = Payment.objects.create(
                order=order,
                amount_paid=payment,
                payment_type=payment_method,
            )

            InstallmentPlan.objects.create(
                payment=payment,
                credit_officer = credit_officer,
                term_months=term_months,
                monthly_due=monthly_due,
                remaining_balance=remaining_balance,
                next_due_date=date.today() + relativedelta(months=1),
                payment_status=Order.ORDER_STATUS[0][0],
            )

            Invoice.objects.create(
                order=order,
                or_number=f"OR-{uuid.uuid4().hex[:8].upper()}",
                vat_amount=order.total_amount * Decimal('0.12'),
                grand_total=order.total_amount,
                issued_by=order.employee
            )

            try:
                sales_agent.total_sales += order.total_amount
                sales_agent.total_commission_earned += (order.total_amount * sales_agent.commission_rate)
                sales_agent.save()

                # //how to save the installment data to credit_officer
            except Exception:
                pass


            return JsonResponse({'success': True, 'order_id': order.id})



        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=405)



@login_required(login_url='login')
def warranty(request, pk):

    sales = get_object_or_404(Order, pk=pk)

    is_manager = request.user.is_superuser or hasattr(request.user, 'employee') and request.user.employee.role == 'Manager'

    if not is_manager:
        raise PermissionDenied

    if request.method == 'POST':
        item_id =  request.POST.get('order_item_id')
        order_item = get_object_or_404(OrderItem, order=sales, id=item_id)
        product = order_item.product

        if request.user.is_superuser:
            inventory_item = BranchInventory.objects.filter(branch=branch, product=product).first()
            if not inventory_item:
                messages.error(request, 'Product not found in any branch inventory')
                return redirect('warranty', pk=pk)
            branch = inventory_item.branch
            handle_by_profile = getattr(request.user, 'employee', None)
        else:
            try:
                employee_profile = request.user.employee
                branch = employee_profile.branch
                inventory_item = BranchInventory.ojects.filter(branch=branch, product=product).first()
                handle_by_profile = employee_profile
            except AttributeError:
                messages.error(request, "You do not have an associated Employee profile.")
                return redirect('warranty', pk=pk)

        faulty_serial = request.POST.get('faulty_serial')
        claim_type = request.POST.get('claim_type')
        issue_description = request.POST.get('issue_description')
        days_since_purchase = (timezone.now() - sales.order_date).days

        if claim_type == 'Replacement' and days_since_purchase > 7:
            messages.error(request, f"Replacement denied. Item is {days_since_purchase} days old (Limit: 7).")
            return redirect('warranty', pk=pk)

        if claim_type == 'Repair' and days_since_purchase > 30:
            messages.error(request, f"Warranty expired. Item is {days_since_purchase} days old (Limit: 30).")
            return redirect('warranty', pk=pk)


        if claim_type == 'Replacement':
            cost_impact = order_item.product.cost_price
            if inventory_item is None:
                messages.error(request, "Branch doesnt have the product.")
                return redirect('warranty', pk=pk)
            elif inventory_item.quantity < 1:
                messages.error(request, "Product out of stock.")
                return redirect('warranty', pk=pk)
        elif claim_type == 'Repair':
            cost_impact = 1500.00
        else:
            cost_impact = 0.00

        existing_claim = WarrantyClaims.objects.filter(order_item=order_item, status__in=['Completed', 'Released']).exists()
        if existing_claim:
            messages.error(request, "Warranty already claimed.")
            return redirect('warranty', pk=pk)

        try:
            with transaction.atomic():
                WarrantyClaims.objects.create(
                    item_id=item_id,
                    order_item=order_item,
                    faulty_serial=faulty_serial,
                    handled_by=handle_by_profile,
                    issue_description=issue_description,
                    cost_impact=cost_impact
                )

                if claim_type == 'Replacement':
                    inventory_item.quantity = F('quantity') - 1
                    inventory_item.save()

                    DefectiveInventory.objects.create(
                        product=product,
                        branch=branch,
                        faulty_serial=faulty_serial,
                        reason=issue_description
                    )
        except Exception as e:
            messages.error(f"Database Error: {e}")
            return redirect('warranty', pk=pk)

        messages.success(request, 'Successful!')
        return redirect('warranty', pk=pk)

    context = {'sales': sales}

    return render(request, 'accounts/warranty.html', context)