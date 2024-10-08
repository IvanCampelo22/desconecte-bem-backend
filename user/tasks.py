from celery import shared_task
from django.template.loader import render_to_string
from .models import User 
from django.core.mail import send_mail
import copy
from notification.models import Notification

@shared_task
def send_email(subject, message):

    active_users = User.objects.filter(is_active=True)

    for user in active_users:
        recipient_email = user.email
        context = copy.deepcopy({
        "name": user.name,
        "subject": subject,
        "message": message,
        "app_name": "Desconecte Bem"
        })
        html_content = render_to_string("daily_message.html", context)
        send_mail(
            subject=subject,
            message=message,
            from_email="desconectebem@gmail.com",
            recipient_list=[recipient_email],
            fail_silently=False,
            html_message=html_content,
        )

        Notification.objects.update_or_create(
        user=user,
        title=f"{len(active_users)} e-mails enviados com sucesso.",
        message=message,
        notification_type="success",  # Assumindo que warning é um tipo adequado
    )
        
