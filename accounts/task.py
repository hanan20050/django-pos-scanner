from django.utils import timezone
from datetime import timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .models import InstallmentPlan


def send_due_reminders():
    target_date = timezone.now().date() + timedelta(days=5)

    plans = InstallmentPlan.objects.filter(
        next_due_date=target_date,
    )

    for plan in plans:
        customer = plan.payment.order.customer
        if customer and customer.email:
            context = {
                'customer_name': customer.name,
                'monthly_due': plan.monthly_due,
                'due_date': plan.next_due_date,
            }
            html_content = render_to_string('emails/due_reminder.html', context)

            email = EmailMessage(
                subject="Upcoming Payment Reminder - Galos Gadget Hub",
                body=html_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[customer.email],
            )
            email.content_subtype = "html"
            email.send()

            # Optional: Mark as sent so we don't spam them
            # plan.reminder_sent = True
            # plan.save()