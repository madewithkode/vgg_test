from vgg_interview.settings.celery import CELERY

from accounts.models import Event, User, Candidate
from datetime import datetime, date, timedelta
from django.core.mail import send_mail

"""
Celery task to send interview reminder to candidate
"""
@CELERY.task(name='send_interview_reminder')
def send_interview_reminder(user_email):

    todays_events = Event.objects.filter(start=datetime.today())
        if todays_events:
            for event in todays_events:
                send_mail(
                    'Interview Reminder',
                    'You have an interview scheduled for {}. Be reminded'.format(event.start.strftime('H:M')),
                    'interviews@vgg.com',
                    [event.candidate.user.email],
                    fail_silently=False,
                )

