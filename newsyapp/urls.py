from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.get_topstories, name="get_topstories"),
]