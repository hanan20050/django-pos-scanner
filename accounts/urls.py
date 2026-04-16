from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('manage_employee/<int:pk>/', views.manageEmployee, name='manage_employee'),

    path('pos_terminal/', views.posTerminal, name='pos_terminal'),
    path('scan_product/', views.scanProduct, name='scan_product'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('branch_inventory', views.branchInventory, name='branch_inventory'),
    path('accounts/<int:pk>/inventory_update', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('employee_profile', views.employeeProfile, name='employee_profile'),
    path('employee_list', views.EmployeeList.as_view(), name='employee_list'),
    path('employee_form', views.EmployeeCreate.as_view(), name='employee_form'),
    # path('pos_terminal', views.posTerminal, name='pos_terminal'),
    path('checkout/cash/', views.checkout_cash, name='checkout_cash'),
    path('checkout/installment/', views.installment_checkout, name='installment_checkout'),
    path('sales_display/', views.salesDisplay, name='sales_display'),
    path('components/<int:pk>/sales_edit', views.salesUpdateView.as_view(), name='sales_edit'),
    path('accounts/<int:pk>/emp_receipt/', views.emp_receipt, name='emp_receipt'),
    path('inst_calculator/', views.instCalculator, name='inst_calculator'),
    path('admin_installment/', views.admin_installment, name='admin_installment'),
    path('accounts/<int:pk>/manage_installment', views.manage_installment, name='manage_installment'),
    path('admin_reports/', views.admin_reports, name='admin_reports'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('warranty/<int:pk>/', views.warranty, name='warranty'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('warrnty_list/', views.warranty_list, name='warranty_list'),
    path('update_claim_status/<int:pk>/', views.update_claim_status, name='update_claim_status'),
    path('audit_logs/', views.audit_logs, name='audit_logs'),
    path('sales_display/export/', views.export_sales_csv, name='export_sales_csv'),
    path('branch_inventory/export/', views.export_branch_inventory_csv, name='export_branch_inventory_csv')
]