import uuid

from django.db import models
from django.utils import timezone
from user.models import User
from django.utils.translation import gettext_lazy as _

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("info", "Informação"),
        ("warning", "Aviso"),
        ("error", "Erro"),
        ("success", "Sucesso"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pendente"),
        ("sent", "Enviada"),
        ("failed", "Falha"),
    ]

    code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    process = models.CharField(max_length=150)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Data de Criação'))


    def mark_as_sent(self):
        self.status = "sent"
        self.sent_at = timezone.now()
        self.save()

    def mark_as_failed(self):
        self.status = "failed"
        self.save()

    def __str__(self):
        return f"{self.title} - {self.notification_type}"

    def view(self):
        return f"{self.title} - {self.notification_type}"

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-created_at"]