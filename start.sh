#!/usr/bin/env bash
# exit on error
set -o errexit

python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth.models import User
from accounts.models import Employee, Branch

# Superuser / Admin
admin_user = os.getenv('ADMIN_USERNAME', 'admin')
admin_pass = os.getenv('ADMIN_PASSWORD', 'admin')
u_admin, created = User.objects.get_or_create(username=admin_user, defaults={'email': 'admin@pharmacy.pk', 'is_staff': True, 'is_superuser': True})
u_admin.set_password(admin_pass)
u_admin.is_staff = True
u_admin.is_superuser = True
u_admin.save()

# Cashier User
cashier_user = os.getenv('CASHIER_USERNAME', 'cashier1')
cashier_pass = os.getenv('CASHIER_PASSWORD', 'cashier123')
branch = Branch.objects.first()

if branch:
    emp_admin, _ = Employee.objects.get_or_create(user=u_admin, defaults={'branch': branch, 'name': 'System Admin', 'role': 'Manager', 'email': u_admin.email})
    emp_admin.role = 'Manager'
    emp_admin.branch = branch
    emp_admin.save()
u, created = User.objects.get_or_create(username=cashier_user, defaults={'email': 'cashier@pharmacy.pk'})
if created or not u.check_password(cashier_pass):
    u.set_password(cashier_pass)
    u.save()

if branch:
    emp, _ = Employee.objects.get_or_create(user=u, defaults={'branch': branch, 'name': 'Render Cashier', 'role': 'Cashier', 'email': u.email})
    emp.role = 'Cashier'
    emp.branch = branch
    emp.save()
"

gunicorn pos.wsgi:application --bind 0.0.0.0:$PORT
