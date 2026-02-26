from django.urls import path
from . import views

urlpatterns = [
    path('manage_employee/<int:pk>/', views.manageEmployee, name='manage_employee'),

    path('pos_terminal/', views.posTerminal, name='pos_terminal'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    path('branch_inventory', views.branchInventory, name='branch_inventory'),
    path('accounts/<int:pk>/inventory_update', views.InventoryUpdateView.as_view(), name='inventory_update'),
    path('employee_profile', views.employeeProfile, name='employee_profile'),
    path('employee_list', views.EmployeeList.as_view(), name='employee_list'),
    path('employee_form', views.EmployeeCreate.as_view(), name='employee_form'),
    # path('pos_terminal', views.posTerminal, name='pos_terminal'),
]