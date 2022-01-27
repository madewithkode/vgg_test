from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from datetime import datetime, time, timedelta
from util.checktime import is_time_between_nine_to_five
from accounts.models import Interviewer
import pytz

class InterviewerRegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    work_start = forms.CharField()
    work_end = forms.CharField()

    def __init__(self, *args, **kwargs):
        """Set up default value for instance objects."""
        self.interviewer_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Handles authentication check."""

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        work_start = datetime.strptime(str(self.cleaned_data.get('work_start')), "%Y-%m-%dT%H:%M")
        work_end = datetime.strptime(str(self.cleaned_data.get('work_end')), "%Y-%m-%dT%H:%M")

        if datetime.now() >= work_end:
            raise forms.ValidationError(
                message="Work end date selected is in the past, Selct a future date", code="invalid_start_date"
            )

class UpdateInterviewerForm(forms.Form):
    work_start = forms.CharField()
    work_end = forms.CharField()

    def __init__(self, *args, **kwargs):
        """
        Set up default value for instance objects.
        """
        self.interviewer_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Sanitizes the form
        """

        work_start = self.cleaned_data.get('work_start')
        work_end = self.cleaned_data.get('work_end')

class CreateEventForm(forms.Form):
    start_date = forms.CharField()
    duration = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateEventForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        Sanitizes the form
        """

        start_date = datetime.strptime(str(self.cleaned_data.get('start_date')), "%Y-%m-%dT%H:%M")
        duration = int(self.cleaned_data.get('duration'))

        interviewer = Interviewer.objects.get(user=self.request.user)

        utc=pytz.UTC
        if datetime.now() >= start_date:
            raise forms.ValidationError(
                message="Event start date selected is in the past, Selct a future date", code="invalid_start_date"
            )

        if utc.localize(start_date) > interviewer.work_end: # check date comes after work duration
            raise forms.ValidationError(
                message="Event start time comes after your work end date"
            )

        if not is_time_between_nine_to_five(start_date.time()): # check is between 9-5(working hours):
            raise forms.ValidationError(
                message="Event start time must be between working hours(9am-5pm)"
            )

        if duration < 1800 or duration > 3600: # check is between 9-5(working hours):
            raise forms.ValidationError(
                message="Duration must be between 1800 Seconds(30 minutes) to 3600 Seconds(1 Hour)"
            )

class InterviewerLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def __init__(self, *args, **kwargs):
        """Set up default value for instance objects."""
        self.candidate_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Handles authentication check."""

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

