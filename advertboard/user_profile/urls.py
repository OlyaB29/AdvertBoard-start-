 # -- coding: utf-8 --
from django.urls import path
from . import views


urlpatterns = [
    path("<int:pk>/", views.ProfileDetailView.as_view()),
    path("update/<int:pk>/", views.ProfileUpdateView.as_view()),
    path("update/avatar/<int:pk>/", views.AvatarUpdateView.as_view()),
]