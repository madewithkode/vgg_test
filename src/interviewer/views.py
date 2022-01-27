from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth import login, logout
from interviewer.forms import  InterviewerLoginForm, InterviewerRegisterForm, CreateEventForm
from lib.authentication import InterviewerLoginRequiredMixin
from candidate.forms import  CandidateLoginForm, CandidateRegisterForm, UpdateCandidateForm
from accounts.models import Event, Candidate, User, Interviewer
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.
class IndexView(View):

    def get(self, request):
        """Render index page."""

        return render(request, 'home.html')

class CreateInterviewerView(View):
    def get(self, request):
        """Render interviewer creation page.
        """

        if request.user.is_authenticated:
            return redirect(reverse('interviewer:candidates_list'))
        form = InterviewerRegisterForm()
        return render(request, 'interviewer_register.html', {'form':form})

    def post(self, request):
        """
        Handle interviewer registration.
        """

        form = InterviewerRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                messages.add_message(request, messages.ERROR, 'Interviewer with same email already exists!')
                return render(request, 'interviewer_register.html', {'form': form})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password']
                )
                interviewer = Interviewer.objects.create(work_start=form.cleaned_data['work_start'], user=user, work_end=form.cleaned_data['work_end'])
                return redirect(reverse('interviewer:interviewer_login'))
        return render(request, 'interviewer_register.html', {'form': form})

class InterviewerLoginView(View):
    def get(self, request):
        """Render interviewer login page.
        """

        if request.user.is_authenticated:
            return redirect(reverse('interviewer:candidates_list'))

        form = InterviewerLoginForm()
        return render(request, 'interviewer_login.html')

    def post(self, request):
        """
        Handle interviewer login.
        """

        form = InterviewerLoginForm(request.POST)
        if form.is_valid():
            interviewer_user = authenticate(email=form.cleaned_data['email'], password=form.cleaned_data['password'])

            if interviewer_user:
                login(request, interviewer_user, backend='lib.authentication.UserBackend')
                return redirect(reverse('interviewer:candidates_list'))

        messages.add_message(request, messages.ERROR, 'Invalid Login Credentials')
        return render(request, 'interviewer_login.html', {'form': form})

class CandidatesListView(InterviewerLoginRequiredMixin, View):
    def get(self, request):
        """Render candidates list page.
        """

        candidates = Candidate.objects.all()
        context = {'candidates':candidates}
        return render(request, 'candidate_list.html', context)

class EventsListView(InterviewerLoginRequiredMixin, View):
    def get(self, request):
        """Render interviewers scheduled events page.
        """
        interviewer = Interviewer.objects.get(user=request.user)
        events = interviewer.booked_events.all()
        context = {'events':events}
        return render(request, 'scheduled_events.html', context)

class CreateEventView(InterviewerLoginRequiredMixin, View):
    def get(self, request, candidate_id):
        """Render event creation page.
        """

        form = CreateEventForm()
        try:
            candidate = Candidate.objects.get(id=candidate_id)
            return render(request, 'create_event.html', {'form': form, 'candidate':candidate})
        except Candidate.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Candidate does not exist!')
            return render(request, 'create_event.html', {'form': form})

    def post(self, request, candidate_id):
        """
        Handle event creation.
        """
        candidate = Candidate.objects.get(id=candidate_id)
        form = CreateEventForm(request.POST, request=request)
        if form.is_valid():
            try:
                event = Event(
                    start=form.cleaned_data['start_date'],
                    duration=int(form.cleaned_data['duration']),
                    candidate=candidate
                    )
                interviewer = Interviewer.objects.get(user=request.user)
                book = interviewer.book(event)
                if book.get('status') == False:
                    messages.add_message(request, messages.ERROR, book.get('message'))
                    return render(request, 'create_event.html', {'form': form, 'candidate':candidate})
                messages.add_message(request, messages.SUCCESS, book.get('message'))
                return redirect(reverse('interviewer:events'))
            except Candidate.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Candidate does not exist')
                return render(request, 'create_event.html', {'form': form})
        return render(request, 'create_event.html', {'form': form, 'candidate':candidate})

class UpdateEventView(InterviewerLoginRequiredMixin, View):
    def get(self, request, event_id):
        """Render event update page.
        """

        form = CreateEventForm()
        try:
            event = Event.objects.get(id=event_id)
            candidate = event.candidate
            return render(request, 'update_event.html', {'form': form, 'candidate':candidate})
        except Candidate.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Candidate does not exist!')
            return render(request, 'update_event.html', {'form': form})

    def post(self, request, event_id):
        """
        Handle event update.
        """

        ev = Event.objects.get(id=event_id)
        candidate = ev.candidate
        form = CreateEventForm(request.POST, request=request)
        if form.is_valid():
            try:
                event = Event(
                    start=form.cleaned_data['start_date'],
                    duration=int(form.cleaned_data['duration']),
                    candidate=candidate
                    )
                interviewer = Interviewer.objects.get(user=request.user)
                book = interviewer.book(event, is_update=True)
                if book.get('status') == False:
                    messages.add_message(request, messages.ERROR, book.get('message'))
                    return render(request, 'create_event.html', {'form': form, 'candidate':candidate})
                messages.add_message(request, messages.SUCCESS, book.get('message'))
                return redirect(reverse('interviewer:events'))
            except Candidate.DoesNotExist:
                messages.add_message(request, messages.ERROR, 'Candidate does not exist')
                return render(request, 'create_event.html', {'form': form})

        return render(request, 'update_event.html', {'form': form, 'candidate':candidate})

class DeleteEventView(InterviewerLoginRequiredMixin, View):
    def get(self, request, event_id):
        """Delete Event
        """
        interviewer = Interviewer.objects.get(user=request.user)
        event = Event.objects.get(id=event_id)
        events = interviewer.booked_events.remove(event)
        event.delete()

        messages.add_message(request, messages.SUCCESS, 'Event Deleted Successfully')
        return redirect(reverse('interviewer:events'))

class InterviewerLogoutView(InterviewerLoginRequiredMixin, View):
    def get(self, request):
        """
        Logout interviewer.
        """

        request.session.flush()
        logout(request)
        return redirect(reverse('interviewer:interviewer_login'))