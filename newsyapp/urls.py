from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.get_stories, name="get_stories"),
    path("jobs/", views.get_jobs, name="get_jobs"),
    path("detail/<int:item_id>", views.get_detail, name="detail"),
    path("sync/", views.sync_db, name="sync_db"),
    path("update/", views.update_stories, name="update_stories"),
]