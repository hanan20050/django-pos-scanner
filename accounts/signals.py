from idlelib.configdialog import changes

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Product, AuditTrail
from .middleware import get_current_user
from .views import employeeProfile

@receiver(pre_save, sender=Product)
def audit_product_logs(sender, instance, **kwargs):
    if not instance.id:
        return

    try:
        old_obj = Product.objects.get(pk=instance.id)
    except Product.DoesNotExist:
        return

    user = get_current_user()
    employee = None
    if user and user.is_authenticated:
        try: employee = user.employee
        except: employee = None

    watch_fields = ['product_name', 'cost_price', 'base_price', 'min_stock_level', 'barcode']
    changes = {}

    for field in watch_fields:
        old_val = getattr(old_obj, field)
        new_val = getattr(instance, field)

        if old_val != new_val:
            changes[field] = {
                'old': str(old_val),
                'new': str(new_val),
            }

    if changes:
        AuditTrail.objects.create(
            user=employee,
            action='UPDATE',
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            change_log=changes
        )


@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    current_user = get_current_user()
    employee = None

    if current_user and current_user.is_authenticated:
        try:
            employee = current_user.employee
        except:
            employee = None

    action = 'CREATE' if created else 'UPDATE'

    if created:
        AuditTrail.objects.create(
            user=employee,
            action=action,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            change_log={
                'name': instance.product_name,
                'cost_price': str(instance.cost_price),
                'base_price': str(instance.base_price),
                'min_stock_level': instance.min_stock_level,
                'barcode': instance.barcode,
                'supplier': str(instance.supplier),
                'category': instance.category,
                'status': 'Created via Admin/System'
            },
        )
        print(f"Audit: Created {instance.product_name}")
    # else:
    #     AuditTrail.objects.create(
    #         user=employee,
    #         action='UPDATE',
    #         content_type=ContentType.objects.get_for_model(instance),
    #         object_id=instance.id,
    #         change_log={
    #             'name': instance.product_name,
    #             'cost_price': str(instance.cost_price),
    #             'base_price': str(instance.base_price),
    #             'min_stock_level': instance.min_stock_level,
    #             'barcode': instance.barcode,
    #             'supplier': str(instance.supplier),
    #             'category': instance.category,
    #             'status': 'Updated via Admin/System'
    #         },
    #     )
    #     print(f"Audit: Updated {instance.product_name}")