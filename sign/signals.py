from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:  # Проверяем, что пользователь создан
        subject = "Добро пожаловать на наш сайт!"
        message = f"Привет, {instance.username}!\n\nСпасибо за регистрацию на нашем сайте."
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )