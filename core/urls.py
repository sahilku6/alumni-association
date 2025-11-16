# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:pk>/', views.profile_detail, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('directory/', views.DirectoryView.as_view(), name='directory'),
    
    # Jobs
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:pk>/applicants/', views.job_applicants, name='job_applicants'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applications/<int:app_id>/update/', views.update_application_status, name='update_application_status'),
    
    # Events
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/my/', views.my_events, name='my_events'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    
    # Stories
    path('stories/', views.SuccessStoryListView.as_view(), name='success_stories'),
    path('stories/create/', views.create_story, name='create_story'),
    path('stories/<int:pk>/', views.SuccessStoryDetailView.as_view(), name='story_detail'),
    
    # Donations
    path('donate/', views.donate, name='donate'),
]
