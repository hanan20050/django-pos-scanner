from http.client import responses

from django.contrib.admin.templatetags.admin_list import items_for_result, paginator_number
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from .models import Product, Employee, Branch, BranchInventory
from .filters import InventoryFilter
from django.core.paginator import Paginator
from django.views.generic.edit import UpdateView, CreateView
from django.urls import reverse_lazy
from .forms import EmployeeForm, EmployeeAdminForm
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db import transaction

from django.http import JsonResponse




# Create your views here.

class InventoryUpdateView(UpdateView):
    model = BranchInventory
    fields = ['quantity']
    template_name = 'accounts/inventory_update.html'
    success_url = reverse_lazy('branch_inventory')


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
def branchInventory(request):
    is_manager = request.user.is_superuser or hasattr(request.user, 'employee') and request.user.employee.role == 'Manager'


    if is_manager:
        items = BranchInventory.objects.all().select_related('branch', 'product')
        assigned_branch = 'All Branches'
    else:
        try:
            login_employee = Employee.objects.get(user=request.user)
            assigned_branch = login_employee.branch

            items = BranchInventory.objects.filter(branch=assigned_branch).select_related('product', 'product__supplier')

        except Employee.DoesNotExist:
            items = BranchInventory.objects.none()
            assigned_branch = 'None assigned'

    myFilter = InventoryFilter(request.GET, queryset=items)
    filtered_items = myFilter.qs

    paginator = Paginator(filtered_items, 10)

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

    context = {'employee':employee, 'branch_products':branch_products}

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