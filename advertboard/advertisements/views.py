from django.db.models import OuterRef, Subquery
from rest_framework import generics, permissions
from . models import Advert, Gallery, Photo
from . serializers import AdvertListSerializer, AdvertDetailSerializer, AdvertCreateUpdateSerializer


class AdvertListView(generics.ListAPIView):
    # Вывод списка объявлений
    permission_classes = [permissions.AllowAny]
    serializer_class = AdvertListSerializer

    def get_queryset(self):
        photo = Photo.objects.filter(gallery__advert=OuterRef("pk"))
        adverts = Advert.objects.filter(moderation=True).annotate(main_photo=Subquery(photo.values('image')[:1]))
        return adverts


class AdvertDetailView(generics.RetrieveAPIView):
    # Вывод подробной информации об объявлении
    queryset = Advert.objects.filter(moderation=True)
    permission_classes = [permissions.AllowAny]
    serializer_class = AdvertDetailSerializer
    lookup_field = 'id'


class AdvertCreateView(generics.CreateAPIView):
    # Добавление объявления
    permission_classes = [permissions.IsAuthenticated]
    queryset = Advert.objects.all()
    serializer_class = AdvertCreateUpdateSerializer


class UserAdvertListView(generics.ListAPIView):
    # Все объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertListSerializer

    def get_queryset(self):
        photo = Photo.objects.filter(gallery__advert=OuterRef("pk"))
        adverts = Advert.objects.filter(user=self.request.user, moderation=True).annotate(main_photo=Subquery(photo.values('image')[:1]))
        return adverts


class UserAdvertUpdateView(generics.RetrieveUpdateAPIView):
    # Редактирование объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AdvertCreateUpdateSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Advert.objects.filter(user=self.request.user)


class UserAdvertDeleteView(generics.DestroyAPIView):
    # Удаление объявления пользователя
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        return Advert.objects.filter(id=self.kwargs.get("pk"), user=self.request.user)