import os
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login

from accounts.models import Interviewer, Candidate, User


class UserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):  # NOQA
        """Authenticate Admin(Interviewer) user
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        # login admin if password match
        if check_password(password, user.password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class InterviewerLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'interviewer:interviewer_login'
    def dispatch(self, request, *args, **kwargs):
        """Handle login required check for Interviewer."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            Interviewer.objects.get(user_id=request.user.id)
            return super().dispatch(request, *args, **kwargs)  # type: ignore
        except Interviewer.DoesNotExist:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

class CandidateLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'candidate:candidate_login'
    def dispatch(self, request, *args, **kwargs):
        """Handle login required check for Candidate."""
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        try:
            Candidate.objects.get(user_id=request.user.id)
            return super().dispatch(request, *args, **kwargs)  # type: ignore
        except Candidate.DoesNotExist:
            return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

