from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.get_stories, name="get_stories"),
    path("jobs/", views.get_jobs, name="get_jobs"),
    path("story_detail/<int:item_id>", views.get_story, name="story_detail"),
    path("job_detail/<int:item_id>", views.get_job, name="job_detail"),
    # path("sync_stories/", views.sync_stories, name="sync_stories"),
    # path("sync_jobs/", views.sync_jobs, name="sync_jobs"),
    # path("update/", views.update_stories, name="update_stories"),
]