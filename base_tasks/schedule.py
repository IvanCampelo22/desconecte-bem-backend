from celery.schedules import crontab
import google.generativeai as genai
import os
from configs.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
response = model.generate_content("Escreva um texto bonito e inspirador para pessoas que precisam sair do celular")

CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "user.tasks.send_email", 
        "schedule": crontab(minute="*/15"),
        "args": ("Mensagem escrita pelo Gemini", response.text)
    },

}
