from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class CandidateRegisterForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    stack = SimpleArrayField(forms.CharField(), required=True)

    def __init__(self, *args, **kwargs):
        """Set up default value for instance objects."""
        self.candidate_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Handles authentication check."""

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

class UpdateCandidateForm(forms.Form):
    name = forms.CharField()
    stack = SimpleArrayField(forms.CharField(), required=True)

    def __init__(self, *args, **kwargs):
        """Set up default value for instance objects."""
        self.candidate_user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        """Handles authentication check."""

        name = self.cleaned_data.get('name')
        stack = self.cleaned_data.get('stack')

class CandidateLoginForm(forms.Form):
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

