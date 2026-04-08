# 🏪 Django POS Scanner System

> A comprehensive, production-ready Point of Sale (POS) management system built with Django for **Galos Gadget Hub** — featuring multi-branch inventory, installment credit management, warranty claims, real-time sales analytics, and role-based employee access.

[![Django CI Check](https://github.com/johnaljennegalos/django-pos-scanner/actions/workflows/django.ci.yml/badge.svg)](https://github.com/johnaljennegalos/django-pos-scanner/actions/workflows/django.ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-6.0.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents

1. [Executive Summary](#-executive-summary)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [Project Structure](#-project-structure)
5. [Setup & Installation](#-setup--installation)
6. [Database Models](#-database-models)
7. [User Roles & Permissions](#-user-roles--permissions)
8. [URL Endpoints](#-url-endpoints)
9. [Key Features Deep Dive](#-key-features-deep-dive)
10. [Configuration & Settings](#-configuration--settings)
11. [Troubleshooting](#-troubleshooting)
12. [Development Guidelines](#-development-guidelines)
13. [Production Deployment](#-production-deployment)
14. [Contributing](#-contributing)
15. [License & Support](#-license--support)

---

## 🏢 Executive Summary

The **Django POS Scanner System** is a full-featured retail management platform designed for **Galos Gadget Hub** — a multi-branch electronics gadget store. It replaces manual sales tracking with a barcode-driven POS terminal, automates installment credit approvals, streamlines warranty processing, and provides real-time analytics for managers.

### Business Value
| Metric | Benefit |
|--------|---------|
| **Sales Speed** | Barcode scan → checkout in seconds |
| **Credit Risk** | Credit Officer approval workflow for every installment |
| **Warranty Handling** | Structured Repair vs Replacement with cost tracking |
| **Inventory Visibility** | Per-branch low-stock alerts with minimum thresholds |
| **Reporting** | Weekly / Monthly / Yearly revenue, commissions, and outstanding balances |
| **Accountability** | Employee login/logout tracking with session timestamps |

---

## ✨ Features

### Core POS Functions
- **Barcode-driven POS Terminal** — scan products to add them to cart in real time
- **Cash Checkout** — automatic change calculation, receipt generation, invoice OR number
- **Installment Checkout** — configurable term (months), monthly due, and balance tracking
- **Order Management** — create, view, soft-delete, and archive sales orders
- **Customer Lookup** — phone-based customer identification (optional for cash sales)

### Advanced Features
- **Warranty Claims** — file Repair or Replacement claims with serial number tracking
  - Repair: 30-day window
  - Replacement: 7-day window with old/new serial swap record
- **Installment Plans** — multi-month schedules with automatic next-due-date progression
- **Invoice Generation** — unique OR numbers, VAT computation, issued-by tracking
- **Commission Tracking** — per-agent rate × total sales, cumulative earnings
- **Defective Inventory** — log faulty units with reason, disposal status, and branch

### Admin & Reporting
- **Admin Dashboard** — real-time KPIs: revenue, cost, gross profit, transaction count
- **Branch Revenue Chart** — bar chart comparison of all branches
- **Employee Sales Chart** — individual sales agent performance
- **Weekly / Monthly / Yearly Totals** — period-based revenue aggregation
- **Outstanding Balance Monitor** — total owed from pending installments
- **Payment Method Breakdown** — cash vs installment revenue split

### Employee Management
- Role-based access: Manager, Sales Agent, Credit Officer
- Login/logout timestamps (`last_login_time`, `last_logout_time`, `is_logged_in`)
- Soft-delete with cascading Django `User.is_active = False`
- Profile pictures, email, phone, branch assignment, hire date

### Multi-Branch Support
- Inventory tracked per branch (`BranchInventory`)
- Orders tagged to the processing branch
- Branch-level revenue reporting
- Soft-deletable branches

### Supplier Management
- Contract start/expiration with automatic `contract_status` property
- Supplier archive/restore actions in admin
- Products linked to suppliers with cascade behavior

---

## 🛠 Tech Stack

### Backend
| Component | Technology | Version |
|-----------|-----------|---------|
| Web Framework | Django | 6.0.2 |
| WSGI Server | asgiref | 3.11.1 |
| Database | SQLite (dev) | — |
| Date Utilities | python-dateutil | 2.9.0.post0 |
| Slug Utilities | python-slugify | 8.0.4 |
| SQL Parsing | sqlparse | 0.5.5 |
| Timezone Data | tzdata | 2025.3 |

### Frontend
| Component | Technology |
|-----------|-----------|
| Template Engine | Django Templates |
| Styling | HTML/CSS (Tailwind utility classes) |
| Barcode Scanning | JavaScript (posScanner.js) |
| POS UI | JavaScript (posTerminal.js, posUI.js, posCalculations.js, posInit.js) |
| Image Preview | JavaScript (image-preview.js) |

### Django Extensions
| Package | Version | Purpose |
|---------|---------|---------|
| django-admin-interface | 0.32.0 | Enhanced admin panel UI |
| django-colorfield | 0.14.0 | Color picker for admin interface |
| django-filter | 25.2 | Advanced queryset filtering |
| Pillow | 12.1.1 | Image processing for product/profile pics |
| six | 1.17.0 | Python 2/3 compatibility utility |
| text-unidecode | 1.3 | Unicode slug support |

---

## 📁 Project Structure

```
django-pos-scanner/
│
├── accounts/                        # Main application
│   ├── migrations/                  # 37 database migrations
│   │   ├── 0001_initial.py
│   │   └── ... (0002–0037)
│   ├── templates/
│   │   ├── accounts/                # Page templates
│   │   │   ├── login.html           # Authentication page
│   │   │   ├── main.html            # Sales agent home
│   │   │   ├── dashboard.html       # Manager/admin dashboard
│   │   │   ├── pos_terminal.html    # POS scanner interface
│   │   │   ├── branch_inventory.html
│   │   │   ├── inventory_update.html
│   │   │   ├── sales_display.html   # Order list with filters
│   │   │   ├── admin_reports.html   # Analytics & charts
│   │   │   ├── admin_installment.html
│   │   │   ├── manage_installment.html
│   │   │   ├── employee_list.html
│   │   │   ├── employee_form.html
│   │   │   ├── employee_profile.html
│   │   │   ├── manage_employee.html
│   │   │   ├── inst_calculator.html
│   │   │   ├── emp_receipt.html     # Receipt/invoice print view
│   │   │   ├── warranty.html        # File a warranty claim
│   │   │   ├── warranty_list.html   # List of all claims
│   │   │   └── navbar.html
│   │   └── components/              # Partial/reusable templates
│   │       ├── cart.html
│   │       ├── cash_modal.html
│   │       ├── installment_modal.html
│   │       ├── pos_product_list.html
│   │       └── sales_edit.html
│   ├── admin.py                     # Django admin registrations & customizations
│   ├── apps.py                      # App configuration
│   ├── decorators.py                # @unauthenticated_user decorator
│   ├── filters.py                   # django-filter FilterSet classes
│   ├── forms.py                     # ModelForm definitions
│   ├── models.py                    # All 14 data models
│   ├── urls.py                      # App-level URL patterns
│   └── views.py                     # All view functions and class-based views
│
├── pos/                             # Django project configuration
│   ├── settings.py                  # Application settings
│   ├── urls.py                      # Root URL configuration
│   ├── wsgi.py                      # WSGI entry point
│   └── asgi.py                      # ASGI entry point
│
├── static/                          # Static assets
│   ├── images/                      # Logos and static images
│   │   ├── ggh-logo.png
│   │   └── logo.PNG
│   └── js/                          # JavaScript modules
│       ├── posTerminal.js           # Main POS terminal controller
│       ├── posScanner.js            # Barcode scanning logic
│       ├── posUI.js                 # UI state management
│       ├── posInit.js               # POS initialization
│       ├── posCalculations.js       # Cart total calculations
│       └── image-preview.js         # Profile/product image preview
│
├── templates/                       # Global templates
│   └── admin/
│       └── base_site.html           # Custom admin branding
│
├── media/                           # User-uploaded files (gitignored)
│   └── media/                       # Product images and profile pictures
│
├── admin-interface/                 # django-admin-interface assets
│
├── .github/
│   └── workflows/
│       └── django.ci.yml            # CI: system check + flake8 linting
│
├── manage.py                        # Django management CLI
├── requirements.txt                 # Python dependencies
└── .gitignore                       # Ignores db.sqlite3, media, env, backups
```

### Model Relationship Diagram

```
Django User (auth)
    │ 1:1
    ▼
Employee ──── Branch (ForeignKey)
    │ 1:1              │ 1:M
    ├──► SalesAgent     └──► BranchInventory ◄── Product ◄── Supplier
    │ 1:1
    └──► CreditOfficer
              │ 1:M
              ▼
         InstallmentPlan ◄────────────────── Payment ◄── Order ◄── Customer
                                                              │
                                                              ▼
                                                          OrderItem ──► Product
                                                              │
                                                              ├──► WarrantyClaims
                                                              │         │ 1:1
                                                              │         └──► ReplacementRecord
                                                              │
                                                         Invoice (OR#)

Product ──► DefectiveInventory ◄── Branch
```

---

## 🚀 Setup & Installation

### Prerequisites

| Requirement | Minimum Version |
|-------------|----------------|
| Python | 3.10+ |
| pip | 23.0+ |
| Git | 2.x |
| Virtual Environment | venv / virtualenv |

### Step-by-Step Installation

**1. Clone the repository**
```bash
git clone https://github.com/johnaljennegalos/django-pos-scanner.git
cd django-pos-scanner
```

**2. Create and activate a virtual environment**
```bash
# Create
python -m venv .venv

# Activate — Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate — Windows (CMD)
.\.venv\Scripts\activate.bat

# Activate — macOS / Linux
source .venv/bin/activate
```

**3. Install all dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Initialize the database**
```bash
python manage.py migrate
```

**5. Create a superuser account**
```bash
python manage.py createsuperuser
# Follow the prompts: username, email, password
```

**6. (Optional) Load sample data**
```bash
python manage.py loaddata data_backup_filtered.json
```

**7. Collect static files** *(required for production; optional for dev)*
```bash
python manage.py collectstatic
```

**8. Start the development server**
```bash
python manage.py runserver
```

Access the app at: **http://127.0.0.1:8000/**
Access the admin at: **http://127.0.0.1:8000/admin/**

### Running Tests

```bash
# Django system check (model integrity, URL conflicts, settings validation)
python manage.py check

# Syntax/style linting
pip install flake8
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

---

## 📊 Database Models

### Complete Model Reference

#### `Customer`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField(100) | Required |
| `email` | EmailField(100) | Optional |
| `address` | CharField(100) | Optional |
| `phone` | CharField(100) | Used for quick lookup at POS |
| `date_created` | DateField | Auto-set on creation |
| `is_active` | BooleanField | Soft delete flag |

#### `Branch`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField(100) | Branch display name |
| `address` | CharField(100) | Optional |
| `phone_number` | CharField(100) | Optional |
| `is_active` | BooleanField | Soft delete via overridden `delete()` |

#### `Employee`
| Field | Type | Notes |
|-------|------|-------|
| `user` | OneToOneField(User) | Linked Django auth user |
| `branch` | ForeignKey(Branch) | Required assignment |
| `name` | CharField(100) | Display name |
| `role` | CharField | `Sales Agent` / `Credit Officer` / `Manager` |
| `email` | EmailField | Optional contact |
| `phone` | CharField(20) | Optional contact |
| `profile_pic` | ImageField | Uploaded to `media/` |
| `hire_date` | DateField | Auto-set on creation |
| `is_active` | BooleanField | Cascades `user.is_active = False` |
| `is_logged_in` | BooleanField | Real-time session tracking |
| `last_login_time` | DateTimeField | Updated on each successful login |
| `last_logout_time` | DateTimeField | Updated on logout |

```python
# Soft delete cascades to Django user
def save(self, *args, **kwargs):
    if not self.is_active and self.user.is_active:
        self.user.is_active = False
        self.user.save()
    super().save(*args, **kwargs)
```

#### `SalesAgent`
| Field | Type | Notes |
|-------|------|-------|
| `employee` | OneToOneField(Employee) | Active employees only |
| `commission_rate` | DecimalField(5,2) | Percentage, e.g. `5.00` = 5% |
| `total_commission_earned` | DecimalField(12,2) | Cumulative |
| `total_sales` | DecimalField(12,2) | Cumulative gross sales |

#### `CreditOfficer`
| Field | Type | Notes |
|-------|------|-------|
| `employee` | OneToOneField(Employee) | Active employees only |
| `approval_limit` | DecimalField(12,2) | Max installment they can approve |
| `security_level` | IntegerField | Authorization tier (default 1) |
| `is_active` | BooleanField | |

#### `Supplier`
| Field | Type | Notes |
|-------|------|-------|
| `name` | CharField(100) | |
| `contact_person` | CharField(100) | |
| `phone` | CharField(100) | |
| `contract_expiration` | DateField | |
| `contract_start` | DateField | Auto-set |
| `status` | CharField | `Active` / `Renewed` / `Opted Out` / `Expired` |
| `is_active` | BooleanField | Soft delete via `soft_delete()` |

Computed properties:
- `contract_status` — returns `'Expired'` if today > expiration, else `status`
- `contract_period` — formatted year range, e.g. `"2024 - 2026"`

#### `Product`
| Field | Type | Notes |
|-------|------|-------|
| `supplier` | ForeignKey(Supplier) | |
| `product_name` | CharField(100) | |
| `category` | CharField | `Laptop` / `Android` / `iPhone` / `Printer` |
| `base_price` | DecimalField(10,2) | Selling price |
| `barcode` | CharField(100) | **Unique**, used for POS scanning |
| `cost_price` | DecimalField(10,2) | For gross profit calculation |
| `min_stock_level` | PositiveIntegerField | Low-stock threshold (default 3) |
| `image` | ImageField | Uploaded to `media/` |
| `is_active` | BooleanField | Soft delete flag |
| `deleted_at` | DateTimeField | Timestamp when soft-deleted |

```python
def soft_delete(self):
    self.is_active = False
    self.deleted_at = timezone.now()
    self.save()
```

#### `BranchInventory`
| Field | Type | Notes |
|-------|------|-------|
| `branch` | ForeignKey(Branch) | Active branches only |
| `product` | ForeignKey(Product) | |
| `quantity` | IntegerField | Current stock count |
| `date_added` | DateTimeField | Auto-set, ordered descending |

#### `Order`
| Field | Type | Notes |
|-------|------|-------|
| `customer` | ForeignKey(Customer) | Optional (null for anonymous) |
| `employee` | ForeignKey(Employee) | Processing employee |
| `branch` | ForeignKey(Branch) | Originating branch |
| `order_date` | DateField | Auto-set on creation |
| `total_amount` | DecimalField(10,2) | Sum of all order items |
| `order_status` | CharField | `Pending` / `Completed` / `Cancelled` |
| `payment_method` | CharField | `CASH` / `INSTALLMENT` |
| `is_active` | BooleanField | Soft delete flag |
| `deleted_at` | DateTimeField | Timestamp when archived |

#### `OrderItem`
| Field | Type | Notes |
|-------|------|-------|
| `order` | ForeignKey(Order) | Active orders only |
| `product` | ForeignKey(Product) | |
| `quantity` | IntegerField | |
| `unit_price` | DecimalField(10,2) | Price at time of sale |
| `cost_price` | DecimalField(10,2) | Cost at time of sale |

Computed property: `line_total = quantity × unit_price`

#### `Payment`
| Field | Type | Notes |
|-------|------|-------|
| `order` | ForeignKey(Order) | Protected from deletion |
| `amount_paid` | DecimalField(10,2) | |
| `date_paid` | DateField | |
| `payment_type` | CharField | `CASH` / `INSTALLMENT` |

#### `CashPayment`
| Field | Type | Notes |
|-------|------|-------|
| `payment` | OneToOneField(Payment) | |
| `cash_received` | DecimalField(10,2) | Amount tendered by customer |
| `change_given` | DecimalField(10,2) | Change returned |

#### `InstallmentPlan`
| Field | Type | Notes |
|-------|------|-------|
| `payment` | OneToOneField(Payment) | |
| `credit_officer` | ForeignKey(CreditOfficer) | Approving officer (nullable) |
| `term_months` | IntegerField | Duration in months |
| `monthly_due` | DecimalField(10,2) | Computed: total ÷ months |
| `remaining_balance` | DecimalField(10,2) | Decremented on each payment |
| `next_due_date` | DateField | Advanced by 1 month per payment |
| `payment_status` | CharField | `Pending` / `Completed` / `Cancelled` |

#### `Invoice`
| Field | Type | Notes |
|-------|------|-------|
| `order` | ForeignKey(Order) | Protected, active orders only |
| `or_number` | CharField(100) | **Unique** official receipt number |
| `invoice_date` | DateField | |
| `vat_amount` | DecimalField(10,2) | |
| `grand_total` | DecimalField(10,2) | |
| `issued_by` | ForeignKey(Employee) | |

#### `WarrantyClaims`
| Field | Type | Notes |
|-------|------|-------|
| `order_item` | ForeignKey(OrderItem) | Related sale item |
| `claim_type` | CharField | `Repair` / `Replacement` |
| `faulty_serial` | CharField(100) | Serial number of defective unit |
| `issue_description` | TextField | Customer-reported problem |
| `status` | CharField | `Pending` → `In-Progress` → `Completed` → `Released` |
| `date_filed` | DateTimeField | Auto-set |
| `resolution_date` | DateTimeField | When resolved |
| `cost_impact` | DecimalField(10,2) | Financial cost to the store |
| `handled_by` | ForeignKey(Employee) | Assigned active employee |

#### `ReplacementRecord`
| Field | Type | Notes |
|-------|------|-------|
| `warranty_claims` | OneToOneField(WarrantyClaims) | |
| `old_serial` | CharField(100) | Faulty unit serial |
| `new_serial` | CharField(100) | Replacement unit serial |
| `replacement_date` | DateTimeField | Auto-set |

#### `DefectiveInventory`
| Field | Type | Notes |
|-------|------|-------|
| `product` | ForeignKey(Product) | |
| `branch` | ForeignKey(Branch) | |
| `faulty_serial` | CharField(100) | |
| `reason` | TextField | |
| `date_received` | DateTimeField | Auto-set |
| `is_disposed` | BooleanField | Whether disposed of (default True) |

---

## 👥 User Roles & Permissions

### Superuser / Admin
- Full access to Django Admin panel at `/admin/`
- Branded as **"Galos Gadget Hub Admin"** / **"Galos POS Portal"**
- Can create, archive, and restore: Branches, Employees, Products, Suppliers, Orders
- Read-only access to: CashPayments, Payments, Invoices, OrderItems
- Custom admin actions replace the default `delete_selected` to prevent hard deletes

### Manager
- Redirected to `dashboard` on login
- Access to:
  - Admin Reports (`/admin_reports/`) — revenue charts, KPI cards
  - Installment Management (`/admin_installment/`) — all plans with filters
  - Sales Display (`/sales_display/`) — full order history
  - Employee List (`/employee_list`) — view all staff
  - Warranty List (`/warrnty_list/`) — all warranty claims
  - Branch Inventory (`/branch_inventory`) — stock across all branches

### Sales Agent
- Redirected to `home` (main.html) on login
- Access to:
  - POS Terminal (`/pos_terminal/`) — full barcode scanning checkout
  - Sales Display — their own orders
  - Employee Profile — update email, phone, profile picture
  - File Warranty Claims (`/warranty/<pk>/`)
  - View personal receipt (`/accounts/<pk>/emp_receipt/`)
  - Installment Calculator (`/inst_calculator/`)

### Credit Officer
- Redirected to `home` on login
- Access to:
  - Manage Installment (`/accounts/<pk>/manage_installment`) — process payments
  - View installment plan details and update `remaining_balance` / `next_due_date`
  - Access to payment forms

---

## 🔌 URL Endpoints

### Authentication
| URL | View | Description |
|-----|------|-------------|
| `GET/POST /login/` | `loginPage` | Employee login with session tracking |
| `POST /logout/` | `logoutPage` | Employee logout, updates `last_logout_time` |

### Main
| URL | View | Description |
|-----|------|-------------|
| `GET /` | `home` | Sales agent dashboard |
| `GET /dashboard/` | `dashboard` | Manager analytics dashboard |
| `GET /employee_profile` | `employeeProfile` | View/edit own profile |
| `GET /manage_employee/<pk>/` | `manageEmployee` | Manager: edit employee |

### POS Terminal
| URL | View | Description |
|-----|------|-------------|
| `GET /pos_terminal/` | `posTerminal` | POS interface with product grid |
| `GET /scan_product/` | `scanProduct` | JSON: lookup product by barcode |
| `POST /checkout/cash/` | `checkout_cash` | Process cash transaction |
| `POST /checkout/installment/` | `installment_checkout` | Create installment order |

### Inventory
| URL | View | Description |
|-----|------|-------------|
| `GET /branch_inventory` | `branchInventory` | View stock with filters |
| `GET/POST /accounts/<pk>/inventory_update` | `InventoryUpdateView` | Update stock quantity |

### Employees
| URL | View | Description |
|-----|------|-------------|
| `GET /employee_list` | `EmployeeList` | List all active employees |
| `GET/POST /employee_form` | `EmployeeCreate` | Create new employee + user |

### Sales
| URL | View | Description |
|-----|------|-------------|
| `GET /sales_display/` | `salesDisplay` | Filtered order list |
| `GET/POST /components/<pk>/sales_edit` | `salesUpdateView` | Edit order status |
| `POST /delete-order/<pk>/` | `delete_order` | Soft-delete an order |
| `POST /delete-product/<pk>/` | `delete_product` | Soft-delete a product |
| `GET /accounts/<pk>/emp_receipt/` | `emp_receipt` | Print/view receipt |

### Installment Management
| URL | View | Description |
|-----|------|-------------|
| `GET /inst_calculator/` | `instCalculator` | Calculate installment terms |
| `GET /admin_installment/` | `admin_installment` | Manager: all installment plans |
| `GET/POST /accounts/<pk>/manage_installment` | `manage_installment` | Process monthly payment |

### Warranty
| URL | View | Description |
|-----|------|-------------|
| `GET/POST /warranty/<pk>/` | `warranty` | File a warranty claim |
| `GET /warrnty_list/` | `warranty_list` | List all warranty claims |
| `POST /update_claim_status/<pk>/` | `update_claim_status` | Advance claim status |

### Reporting
| URL | View | Description |
|-----|------|-------------|
| `GET /admin_reports/` | `admin_reports` | Revenue analytics, charts |

### Admin (Django built-in)
| URL | Description |
|-----|-------------|
| `/admin/` | Django Admin Panel |
| `/admin/accounts/branch/` | Branch management |
| `/admin/accounts/employee/` | Employee management |
| `/admin/accounts/product/` | Product catalog |
| `/admin/accounts/order/` | Order management |
| `/admin/accounts/supplier/` | Supplier contracts |
| `/admin/accounts/creditofficer/` | Credit officer management |
| `/admin/accounts/salesagent/` | Sales agent management |
| `/admin/accounts/warrantyclaims/` | Warranty claims |
| `/admin/accounts/defectiveinventory/` | Defective stock |

---

## 🔍 Key Features Deep Dive

### 1. Login & Employee Session Tracking

On every successful login, the system:
1. Authenticates using Django's `authenticate()`
2. Sets `employee.is_logged_in = True`
3. Records `employee.last_login_time = timezone.now()`
4. Redirects based on role: Managers/Superusers → `dashboard`, others → `home`

```python
if user is not None:
    login(request, user)
    if hasattr(user, 'employee'):
        employee = user.employee
        employee.is_logged_in = True
        employee.last_login_time = timezone.now()
        employee.save()

    is_manager = (user.employee.role == 'Manager') if hasattr(user, 'employee') else False
    return redirect('dashboard' if (user.is_superuser or is_manager) else 'home')
```

On logout, `last_logout_time` is set and `is_logged_in` is cleared.

### 2. POS Terminal with Barcode Scanning

The POS terminal at `/pos_terminal/` works as follows:
1. The JavaScript scanner (`posScanner.js`) listens for barcode input
2. It calls `/scan_product/?barcode=<value>` which returns JSON with product info
3. `posUI.js` renders the item in the cart; `posCalculations.js` updates totals
4. The operator selects Cash or Installment checkout

### 3. Cash Checkout Process

```
POST /checkout/cash/
  → Validate cart data (JSON)
  → Create/look up Customer by phone
  → Create Order (CASH, Pending→Completed)
  → Create OrderItem(s), deduct BranchInventory
  → Create Payment + CashPayment (cash_received, change_given)
  → Create Invoice with unique OR number
  → Update SalesAgent.total_sales + commission
  → Return invoice PK for receipt redirect
```

### 4. Installment Checkout

```
POST /checkout/installment/
  → Validate cart + customer + term
  → Create Customer (if new)
  → Create Order (INSTALLMENT, Pending)
  → Create OrderItem(s), deduct BranchInventory
  → Create Payment + InstallmentPlan
     - monthly_due = total / term_months
     - next_due_date = today + 1 month
     - remaining_balance = total
  → Create Invoice
  → Update SalesAgent totals
```

### 5. Warranty Claims

- **Filing**: Sales agent goes to `/warranty/<order_item_pk>/`, selects claim type, enters serial number and issue description
- **Repair flow**: Status: `Pending` → `In-Progress` → `Completed` → `Released`
- **Replacement flow**: Same status progression; on completion a `ReplacementRecord` is created with old/new serial numbers; defective unit added to `DefectiveInventory`
- **Cost impact**: Tracked per claim for financial reporting

### 6. Inventory Management

- Each `Product` has a `min_stock_level` threshold
- `BranchInventory` tracks `quantity` per branch
- `InventoryFilter` supports filtering by: stock status (low/out/in stock), product name, barcode, branch
- Stock is automatically decremented during checkout (wrapped in `transaction.atomic()`)

### 7. Commission Calculations

When an order is completed, the system updates the Sales Agent's profile:

```python
# Automatic commission update on sale completion
if agent:
    agent.total_sales += order.total_amount
    agent.total_commission_earned += (order.total_amount * agent.commission_rate / 100)
    agent.save()
```

### 8. Invoice Generation

Invoices use a unique OR number generated via `get_random_string()` with a standardized prefix. VAT is computed and stored separately. The receipt view at `/accounts/<pk>/emp_receipt/` renders a printable invoice.

### 9. Admin Dashboard Analytics

The `admin_reports` view computes:
- 30-day transaction window
- Total revenue, total cost, and gross profit (via `Sum(F('unit_price') * F('quantity'))`)
- Weekly / Monthly / Yearly totals
- Outstanding installment balances
- Cash vs installment payment breakdown
- Per-branch and per-employee revenue for chart rendering

---

## ⚙️ Configuration & Settings

### Key Settings (`pos/settings.py`)

```python
# Timezone — set to Philippine Standard Time
TIME_ZONE = 'Asia/Manila'
USE_TZ = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static & Media
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Installed Apps
INSTALLED_APPS = [
    "admin_interface",   # Must be before django.contrib.admin
    "colorfield",
    'django.contrib.admin',
    ...
    'accounts',
    'django_filters',
    'django.contrib.humanize'
]
```

### Environment Variables

For production, set these via environment variables or a `.env` file (never commit them):

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | A 50-char random string |
| `DEBUG` | Debug mode flag | `False` in production |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | Production DB connection | `postgres://user:pass@host/db` |

### Switching to PostgreSQL (Production)

```python
# Install: pip install psycopg2-binary
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

---

## 🐛 Troubleshooting

### Database Issues

**Problem**: `django.db.utils.OperationalError: no such table`
```bash
# Reset and re-migrate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Problem**: Migration conflicts
```bash
python manage.py migrate --run-syncdb
# Or reset migrations for the accounts app:
python manage.py migrate accounts zero
python manage.py migrate accounts
```

### Login Problems

**Problem**: User cannot log in despite correct credentials

Checklist:
1. Verify `user.is_active = True` in Django Admin → Users
2. Verify `employee.is_active = True` for the corresponding Employee record
3. Ensure the Employee has a `branch` assigned
4. Check terminal output for `Status update failed:` errors

**Problem**: User logs in but sees wrong page
- Managers must have `employee.role == 'Manager'`
- Superusers always go to `dashboard`
- All other roles go to `home`

### Employee Profile Missing Error

**Problem**: `RelatedObjectDoesNotExist: User has no employee`
- The `user` exists in Django Auth but has no linked `Employee` record
- Fix: Create the Employee in Django Admin and link it to the user

### File Upload Issues

**Problem**: Profile pictures or product images not displaying
```bash
# Ensure MEDIA_ROOT exists
mkdir -p media/media

# Verify settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Verify pos/urls.py has static serving in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
# Ensure STATICFILES_DIRS points to the correct path
```

### Installment Balance Not Decreasing

- Verify the `manage_installment` view is being called via `POST`
- Check that `remaining_balance` >= `monthly_due` before processing
- Ensure the `InstallmentPlan` has `payment_status = 'Pending'`

---

## 🧑‍💻 Development Guidelines

### Coding Standards

- Follow [PEP 8](https://pep8.org/) for Python code style
- Use Django class-based views for list/update operations, function-based views for complex logic
- Wrap multi-step database operations in `transaction.atomic()`
- Use `select_related()` and `prefetch_related()` to avoid N+1 queries

### Soft Delete Pattern

All major models use soft deletes — **never hard-delete production data**:

```python
# Pattern used across Branch, Employee, Product, Order, Supplier
def soft_delete(self):
    self.is_active = False
    self.deleted_at = timezone.now()   # where applicable
    self.save()

# Always filter active records in querysets
Product.objects.filter(is_active=True)
Order.objects.filter(is_active=True)
```

### Database Transaction Handling

```python
from django.db import transaction

@transaction.atomic
def checkout_cash(request):
    # All operations succeed or all roll back
    order = Order.objects.create(...)
    for item in cart_items:
        OrderItem.objects.create(order=order, ...)
        BranchInventory.objects.filter(...).update(quantity=F('quantity') - item['qty'])
    Payment.objects.create(...)
    CashPayment.objects.create(...)
    Invoice.objects.create(...)
```

### Commission Calculation Logic

```python
# commission_rate is stored as a percentage (e.g., 5.00 = 5%)
commission_earned = order.total_amount * Decimal(agent.commission_rate) / Decimal('100')
agent.total_commission_earned += commission_earned
agent.total_sales += order.total_amount
agent.save()
```

### Warranty Business Rules

| Claim Type | Time Window | Action Required |
|------------|-------------|----------------|
| Repair | 30 days from sale | Log faulty serial, track cost impact |
| Replacement | 7 days from sale | Create `ReplacementRecord`, log `DefectiveInventory` |

Status flow: `Pending` → `In-Progress` → `Completed` → `Released`

### Filter Classes

The system uses `django-filter` for dynamic queryset filtering:

```python
# filters.py
class InventoryFilter(django_filters.FilterSet):
    stock_status = django_filters.ChoiceFilter(method='filter_stock_status')

    def filter_stock_status(self, queryset, name, value):
        if value == 'low':
            return queryset.filter(quantity__gt=0, quantity__lte=F('product__min_stock_level'))
        elif value == 'out':
            return queryset.filter(quantity__lte=0)
        elif value == 'in stock':
            return queryset.filter(quantity__gt=F('product__min_stock_level'))
        return queryset
```

---

## 🚢 Production Deployment

### Pre-Deployment Security Checklist

- [ ] Set `DEBUG = False`
- [ ] Generate a new `SECRET_KEY` (never use the development key)
- [ ] Set `ALLOWED_HOSTS` to your domain(s)
- [ ] Switch to PostgreSQL or another production database
- [ ] Configure a reverse proxy (nginx/Apache)
- [ ] Set up HTTPS/TLS certificate
- [ ] Configure `SECURE_SSL_REDIRECT = True`
- [ ] Set `SESSION_COOKIE_SECURE = True`
- [ ] Set `CSRF_COOKIE_SECURE = True`
- [ ] Run `python manage.py check --deploy`

### Deployment Steps

```bash
# 1. Set environment variables
export SECRET_KEY="your-new-secure-secret-key"
export DEBUG=False
export ALLOWED_HOSTS="yourdomain.com,www.yourdomain.com"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply database migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Create superuser (first time only)
python manage.py createsuperuser

# 6. Run system checks
python manage.py check --deploy

# 7. Start with gunicorn (example)
pip install gunicorn
gunicorn pos.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

### Production `settings.py` Additions

```python
# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files (serve via nginx in production)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

---

## 🤝 Contributing

### Branch Naming Convention

```
feature/<short-description>     # New features
fix/<short-description>         # Bug fixes
chore/<short-description>       # Maintenance, refactoring
docs/<short-description>        # Documentation only
```

### Workflow

1. **Fork** the repository (external contributors) or create a branch (team members)
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** following the coding standards above

3. **Verify locally**
   ```bash
   python manage.py check
   flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
   ```

4. **Commit** with a clear message
   ```bash
   git commit -m "feat: add commission breakdown to admin reports"
   ```

5. **Push** and open a Pull Request to `main`
   ```bash
   git push origin feature/your-feature-name
   ```

6. PR will trigger the **Django CI Check** workflow automatically:
   - `python manage.py check`
   - `flake8` syntax/undefined-name check

### Commit Message Format

```
<type>: <short summary>

Types: feat | fix | docs | style | refactor | chore | test
```

---

## 📄 License & Support

## License
This project is licensed under the **CC BY-NC-SA 4.0**. 
- **Non-Commercial:** You may not use this material for commercial purposes.
- **Attribution:** You must give appropriate credit to the original author.
- **ShareAlike:** If you remix or transform the material, you must distribute your contributions under the same license.


### Support & Contact

| Channel | Details |
|---------|---------|
| **Issues** | [GitHub Issues](https://github.com/johnaljennegalos/django-pos-scanner/issues) |
| **Repository** | [github.com/johnaljennegalos/django-pos-scanner](https://github.com/johnaljennegalos/django-pos-scanner) |

### Reporting Bugs

When opening an issue, please include:
1. Python and Django version (`python --version`, `django-admin --version`)
2. Steps to reproduce
3. Expected vs actual behavior
4. Relevant error messages or stack traces

---

<div align="center">

**Galos Gadget Hub POS System** • Built with ❤️ using Django 6.0.2

*Last Updated: April 2026 • Version 1.0.0*

</div>
