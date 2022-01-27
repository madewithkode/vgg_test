from django.urls import path
from candidate.views import (
    CandidateLoginView,
    CandidateLogoutView,
    EditCandidateView,
    RegisterCandidateView,
    CandidateEventsView,
    CandidateDetailsView
)


urlpatterns = [
    path('register/', RegisterCandidateView.as_view(), name='register_candidate'),
    path('login/', CandidateLoginView.as_view(), name='candidate_login'),
    path('<uuid:candidate_id>/events/', CandidateEventsView.as_view(), name='candidate_events'),
    path('<uuid:candidate_id>/', CandidateDetailsView.as_view(), name='candidate_details'),
    path('<uuid:candidate_id>/edit/', EditCandidateView.as_view(), name='edit_details'),
    path('logout/', CandidateLogoutView.as_view(), name='logout_candidate')
]