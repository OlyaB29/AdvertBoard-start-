from django.db.models import OuterRef, Subquery
from rest_framework.response import Response
from rest_framework.views import APIView
from . models import Advert, Gallery, Photo
from . serializers import AdvertListSerializer, AdvertDetailSerializer


class AdvertListView(APIView):
    # Вывод списка объявлений
    def get(self, request):
        photo = Photo.objects.filter(gallery__advert=OuterRef("pk"))
        adverts = Advert.objects.filter(moderation = True).annotate(main_photo=Subquery(photo.values('image')[:1]))
        serializer = AdvertListSerializer(adverts, many=True)
        return Response(serializer.data)


class AdvertDetailView(APIView):
    # Вывод подробной информации об объявлении
    def get(self, request, pk):
        advert = Advert.objects.get(id=pk, moderation=True)
        serializer = AdvertDetailSerializer(advert)
        return Response(serializer.data)
