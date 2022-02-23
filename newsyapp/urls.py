from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("stories/", views.stories, name="stories"),
    path("api/get_stories/", views.get_stories, name="get_stories"),
    path("jobs/", views.jobs, name="jobs"),
    path("api/get_jobs/", views.get_jobs, name="get_jobs"),
    path("story_detail/<int:item_id>", views.get_story, name="story_detail"),
    path("job_detail/<int:item_id>", views.get_job, name="job_detail"),
]