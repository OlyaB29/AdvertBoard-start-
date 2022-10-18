from rest_framework import generics, permissions

from . models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, AvatarUpdateSerializer


class ProfileDetailView(generics.RetrieveAPIView):
    # Профиль пользователя
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    # Редактирование профиля пользователя
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer


class AvatarUpdateView(generics.UpdateAPIView):
    # Редактирование аватара профиля пользователя
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = AvatarUpdateSerializer