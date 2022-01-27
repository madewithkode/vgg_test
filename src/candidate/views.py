from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import login, logout
from candidate.forms import  CandidateLoginForm, CandidateRegisterForm, UpdateCandidateForm
from accounts.models import User, Candidate, Event
from lib.authentication import CandidateLoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import datetime, time, timedelta

# Create your views here.
class RegisterCandidateView(View):
    def get(self, request):
        """Render candidate Registration page.
        """
        if request.user.is_authenticated:
            return redirect(reverse('candidate:candidate_events', args=[request.user.id]))
        form = CandidateRegisterForm()
        return render(request, 'register_candidate.html', {'form':form})

    def post(self, request):
        """
        Handle candidate registration.
        """

        form = CandidateRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                messages.add_message(request, messages.ERROR, 'Candidate with same email already exists!')
                return render(request, 'register_candidate.html', {'form': form})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                candidate = Candidate.objects.create(name=form.cleaned_data['name'], user=user, stack=request.POST.getlist('stack'))
                return redirect(reverse('candidate:candidate_login'))

        return render(request, 'register_candidate.html', {'form': form})

class CandidateLoginView(View):
    def get(self, request):
        """Render candidate login page.
        """

        if request.user.is_authenticated:
            return redirect(reverse('candidate:candidate_events', args=[request.user.id]))

        form = CandidateLoginForm()
        return render(request, 'login_candidate.html')

    def post(self, request):
        """
        Handle candidate login.
        """

        form = CandidateLoginForm(request.POST)
        if form.is_valid():
            candidate_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if candidate_user:
                login(request, candidate_user, backend='lib.authentication.UserBackend')
                return redirect(reverse('candidate:candidate_events', args=[candidate_user.id]))

        messages.add_message(request, messages.ERROR, 'Invalid Login Credentials')
        return render(request, 'login_candidate.html', {'form': form})

class CandidateDetailsView(CandidateLoginRequiredMixin, View):
    def get(self, request, candidate_id):
        """
        Render Candidate details page.
        """

        candidate = Candidate.objects.get(user=request.user)
        context = {'candidate': candidate}

        return render(request, 'candidate_details.html', context)

class CandidateEventsView(CandidateLoginRequiredMixin, View):
    def get(self, request, candidate_id):
        """
        Render Candidate's events page.
        """

        candidate = Candidate.objects.get(user=request.user)
        upcoming_event = Event.objects.filter(candidate=candidate)
        context = {'upcoming_events':upcoming_event}
        return render(request, 'candidate_events.html', context)


class EditCandidateView(CandidateLoginRequiredMixin, View):
    """
    Edit a Candidate object
    """

    def get(self, request, candidate_id):

        form = UpdateCandidateForm()
        candidate = Candidate.objects.get(user=request.user)
        context = {'form':form, 'candidate':candidate}
        return render(request, 'edit_candidate.html', context)

    def post(self, request, candidate_id):
        form = UpdateCandidateForm(request.POST)
        candidate = Candidate.objects.get(user=request.user)
        if form.is_valid():
            candidate.name = form.cleaned_data['name']
            candidate.required_passes = request.POST.getlist('stack')
            candidate.save()
            messages.add_message(request, messages.SUCCESS, 'Candidate updated successfully')
            return redirect(reverse('candidate:candidate_details', args=[candidate.id]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating candidate, please select relevant fields')
            return redirect(reverse('candidate:edit_details', args=[candidate.id]))
        context = {'form':form, 'candidate':candidate}
        return render(request, 'edit_candidate.html', context)


class CandidateLogoutView(CandidateLoginRequiredMixin, View):
    def get(self, request):
        """
        Logout candidate.
        """

        print('This rannnnnnnnnnnn')

        request.session.flush()
        logout(request)
        return redirect(reverse('candidate:candidate_login'))