 # -- coding: utf-8 --
from django.urls import path
from . import views


urlpatterns = [
    path('adverts/', views.AdvertListView.as_view()),
    path('adverts/<int:pk>', views.AdvertDetailView.as_view()),
]