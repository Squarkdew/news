from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.timezone import now
from .models import Post
from django.db.models.signals import m2m_changed

@receiver(pre_save, sender=Post)
def check_daily_limit(sender, instance, **kwargs):
    """Проверяет, не превысил ли автор лимит публикаций (3 в сутки)."""
    if instance.pk is None:  # Только при создании нового поста
        today_news_count = Post.objects.filter(
            author=instance.author, created_at__date=now().date()
        ).count()

        if today_news_count >= 3:
            raise ValidationError("Вы не можете публиковать более 3 новостей в сутки.")




@receiver(m2m_changed, sender=Post.categories.through)
def notify_subscribers(sender, instance, action, **kwargs):
    if action == "post_add":  
        subscribers = set()

        for category in instance.categories.all():
            subscribers.update(category.subscribers.all())  

        if subscribers:
            subject = f"Новая публикация: {instance.title}"
            html_content = render_to_string("email_notification.html", {"post": instance})

            for user in subscribers:
                msg = EmailMultiAlternatives(
                    subject=subject,
                    body='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()