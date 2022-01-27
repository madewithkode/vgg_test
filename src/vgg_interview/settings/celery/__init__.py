import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vgg_interview.settings.dev')


CELERY = Celery('vgg_interview')

CELERYBEAT_SCHEDULE = {
    # Task that runs at the begining of each day to send interview reminders
    'send_interview_reminder': {
        'task': 'send_interview_reminder',
        'schedule': crontab(hour=0, minute=0),
    },
}


CELERY.config_from_object('django.conf:settings')
CELERY.conf.update(CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE)
CELERY.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
