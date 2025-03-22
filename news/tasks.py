from celery import shared_task
from django.utils.timezone import now, timedelta
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Category

@shared_task
def send_post_notification(post_id):
    """Отправляет email-подписчикам при публикации новой статьи"""
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()
    
    subscribers = set()
    for category in categories:
        subscribers.update(category.subscribers.all())

    subject = post.title
    for user in subscribers:
        html_content = render_to_string('email_notification.html', {'post': post, 'user': user})
        
        msg = EmailMultiAlternatives(
            subject=subject,
            body=f"Здравствуй, {user.username}. Новая статья в твоём разделе!",
            from_email='noreply@newsportal.com',
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()



@shared_task
def send_weekly_newsletter():
    """Отправляет подписчикам подборку новостей за последнюю неделю."""
    last_week = now() - timedelta(days=7)

    categories = Category.objects.all()
    for category in categories:
        posts = Post.objects.filter(categories=category, created_at__gte=last_week)
        if posts.exists():
            subscribers = category.subscribers.all()
            for user in subscribers:
                subject = f"Новые статьи в разделе '{category.name}'"
                html_content = render_to_string("weekly_newsletter.html", {"posts": posts, "user": user})

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=f"Здравствуйте, {user.username}! Ознакомьтесь с новыми публикациями в разделе '{category.name}'.",
                    from_email='noreply@newsportal.com',
                    to=[user.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()