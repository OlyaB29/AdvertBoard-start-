 # -- coding: utf-8 --
from django.urls import path
from . import views



urlpatterns = [
    path('', views.AdvertListView.as_view()),
    path('adverts/<int:id>', views.AdvertDetailView.as_view()),
    path('create/', views.AdvertCreateView.as_view()),
    path('adverts/', views.UserAdvertListView.as_view()),
    path('update-advert/<int:id>', views.UserAdvertUpdateView.as_view()),
    path('delete-advert/<int:id>', views.UserAdvertDeleteView.as_view()),
]