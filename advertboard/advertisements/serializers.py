 # -- coding: utf-8 --
from rest_framework import serializers
from . models import Advert, Gallery, Photo, Value


class PhotoSerializer(serializers.ModelSerializer):
    # Фотографии
    class Meta:
        model = Photo
        fields = ('image',)


class GallerySerializer(serializers.ModelSerializer):
    # Галереи фотографий
    photos = PhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = ("photos",)


class ValueSerializer(serializers.ModelSerializer):
    # Значения характеристик
    characteristic = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Value
        fields = "__all__"


class AdvertListSerializer(serializers.ModelSerializer):
    # Список объявлений
    main_photo = serializers.ImageField()

    class Meta:
        model = Advert
        fields = ('title', 'price', 'is_new', 'region', 'place', 'main_photo')


class AdvertDetailSerializer(serializers.ModelSerializer):
    # Подробная информация об объявлении
    category = serializers.StringRelatedField(read_only=True)
    region = serializers.SlugRelatedField(slug_field='title', read_only=True)
    place = serializers.SlugRelatedField(slug_field='city', read_only=True)
    charvalues = ValueSerializer(many=True)
    gallery = GallerySerializer()
    class Meta:
        model = Advert
        exclude = ('moderation',)

