from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .models import User 
import google.generativeai as genai
import os
from configs.config import GEMINI_API_KEY, EMAIL_HOST_USER

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Escreva um texto bonito e inspirador para pessoas que precisam sair do celular")


@shared_task
def send_email(subject, message):
    DAILY_MESSAGE_TEMPLATE_PATH = "./email/template/daily_message.html"
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        recipient_email = user.email
        recipient_name = user.name
        html_template = render_to_string(DAILY_MESSAGE_TEMPLATE_PATH, {
            'name': recipient_name,
            'content': message,
            'title': subject,
            'app_name': "Desconecte Bem"
            
        })
        email = EmailMessage(
            subject,
            message,
            EMAIL_HOST_USER,  
            [recipient_email],
        )
        email.content_subtype = "html"
        email.send()

    print(f"{len(active_users)} e-mails enviados com sucesso.")