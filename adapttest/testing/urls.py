from django.urls import path, re_path

from .views import *

app_name = 'testing'

urlpatterns = [
    re_path(r'^$', index, name='index'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('subjects/', SubjectListView.as_view(), name='subjects'),
    path('subject/<slug:subject_slug>/start/', StartSession, name='start_session'),
    path('subject/<slug:subject_slug>/question/<int:question_pk>/<int:session_pk>', GetQuestion, name='question'),
    path('subject/<slug:subject_slug>', show_subject, name='subject-detail'),
    path('subject/<int:session_pk>/endsession', EndSession, name='end_session')
]
