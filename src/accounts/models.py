from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from lib.base_model import AdminUserManager, BaseAbstractModel
from django.contrib.auth.hashers import check_password
from django.contrib.postgres.fields import ArrayField
from util.checktime import is_time_between_nine_to_five
from datetime import datetime, time, timedelta
import pytz

from django.conf import settings

class User(AbstractBaseUser):
    """Model representation for an Admin(Interviewer)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    objects = AdminUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Respresentation of Interviewer."""

    def authenticate(self, password):  # NOQA
        """Authenticate Candidate user
        """
        # login candidate user if password match
        if check_password(password, self.password):
            return True
        return False

class Interviewer(models.Model):
    """Model representation for an Admin(Interviewer)
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    work_start = models.DateTimeField()
    work_end = models.DateTimeField()
    booked_events = models.ManyToManyField('Event',related_name='interviewers_events')

    def __str__(self):
        """Respresentation of Interviewer.
        """

        return 'VGG Interviewer - {}'.format(self.user.email)

    def book(self, event_obj, is_update=False):
        """function to book a candidate for an event(interview)
        that is within working times and does not intersect with
        already booked events.

        Args:
            Event (Event): Event Object
        """
        utc=pytz.UTC
        interviewers_events = self.booked_events.all()
        current_event_duration = datetime.strptime(event_obj.start, "%Y-%m-%dT%H:%M") + timedelta(seconds=event_obj.duration)
        for event in interviewers_events:
            existing_event_duration = event.start + timedelta(seconds=event.duration)
            if existing_event_duration == utc.localize(current_event_duration): # check no booked event duration clashes
                return {'status':False, 'message':'You already have an event booked for same duration'}
        try:
            #check if candidate has an event scheduled already
            ev = Event.objects.get(
                candidate=event_obj.candidate
            )
            if is_update:
                ev.start = event_obj.start
                ev.duration = event_obj.duration
                ev.save()
                return {'status':True, 'message':'Event updated sucessfully!'}
            return {'status':False, 'message':'Candidate already has an event scheduled.'}
        except Event.DoesNotExist:
            ev = Event.objects.create(
                start=event_obj.start,
                duration=int(event_obj.duration),
                candidate=event_obj.candidate
            )
            self.booked_events.add(ev)
            return {'status':True, 'message':'Event created successfully!'}

class Candidate(AbstractBaseUser):
    """Model representation for a Candidate
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    stack = ArrayField(models.CharField(max_length=100), null=True)


    def __str__(self):
        """Representation of Candidate.
        """

        return 'VGG Candidate - {}'.format(self.user.email)


# DB Model representing an Event
class Event(BaseAbstractModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    start = models.DateTimeField()
    duration = models.IntegerField() # This is in seconds
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE)

