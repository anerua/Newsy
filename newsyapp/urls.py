from django.urls import path
from newsyapp import views

urlpatterns = [
    path("", views.home, name="home"),
]