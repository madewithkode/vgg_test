from django.urls import path
from interviewer.views import (
    InterviewerLoginView,
    CandidatesListView,
    EventsListView,
    CreateInterviewerView,
    CreateEventView,
    UpdateEventView,
    DeleteEventView,
    InterviewerLogoutView
)

urlpatterns = [
    path('login/', InterviewerLoginView.as_view(), name='interviewer_login'),
    path('logout/', InterviewerLogoutView.as_view(), name='interviewer_logout'),
    path('candidate_list/', CandidatesListView.as_view(), name='candidates_list'),
    path('events/', EventsListView.as_view(), name='events'),
    path('register/', CreateInterviewerView.as_view(), name='register_interviewer'),
    path('<uuid:candidate_id>/create_event/', CreateEventView.as_view(), name='create_event'),
    path('<uuid:event_id>/update_event/', UpdateEventView.as_view(), name='update_event'),
    path('delete_event/<uuid:event_id>/', DeleteEventView.as_view(), name='delete_event'),

]