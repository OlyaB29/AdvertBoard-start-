# -- coding: utf-8 --
from rest_framework import serializers
from django.contrib.auth.models import User
from . models import *


class UserSerializer(serializers.ModelSerializer):
    # Сериализация пользователя
    class Meta:
        model = User
        fields = ("username", "email")


class ProfileSerializer(serializers.ModelSerializer):
    # Профиль пользователя
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ("user", "name", "phone", "avatar")


class ProfileUpdateSerializer(serializers.ModelSerializer):
    # Редактирование профиля пользователя"""

    class Meta:
        model = Profile
        fields = ("avatar", "phone", "name")


class AvatarUpdateSerializer(serializers.ModelSerializer):
    # Редактирование аватар пользователя
    class Meta:
        model = Profile
        fields = ("avatar",)