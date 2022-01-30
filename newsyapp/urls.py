from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.get_stories, name="get_stories"),
    path("jobs/", views.get_jobs, name="get_jobs"),
    path("sync/", views.sync_db, name="sync_db"),
]