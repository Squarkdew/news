import os
from celery import Celery

from celery.schedules import crontab

 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
 
app = Celery('news')
app.config_from_object('django.conf:settings', namespace = 'CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'news.tasks.send_weekly_newsletter',
        'schedule': crontab(day_of_week=6, hour=18, minute=0),  
    },
}