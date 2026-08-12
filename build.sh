#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth.models import User
from accounts.models import Employee, Branch

# Superuser / Admin
admin_user = os.getenv('ADMIN_USERNAME', 'admin')
admin_pass = os.getenv('ADMIN_PASSWORD', 'admin123')
if not User.objects.filter(username=admin_user).exists():
    User.objects.create_superuser(admin_user, 'admin@pharmacy.pk', admin_pass)

# Cashier User
cashier_user = os.getenv('CASHIER_USERNAME', 'cashier1')
cashier_pass = os.getenv('CASHIER_PASSWORD', 'cashier123')
branch = Branch.objects.first()
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
