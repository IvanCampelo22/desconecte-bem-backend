from celery import shared_task
from django.core.mail import EmailMessage
from .models import User 
import google.generativeai as genai
import os
from configs.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Escreva um texto bonito e inspirador para pessoas que precisam sair do celular")


@shared_task
def send_email(subject, messagem):
    active_users = User.objects.filter(is_active=True)
    for user in active_users:
        recipient_email = user.email
        email = EmailMessage(
            subject,
            messagem,
            "ivancampelo1973@gmail.com",  
            [recipient_email]
        )
        email.content_subtype = "html"
        email.send()

    print(f"{len(active_users)} e-mails enviados com sucesso.")