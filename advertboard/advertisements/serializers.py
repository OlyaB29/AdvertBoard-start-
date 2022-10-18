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
    category = serializers.StringRelatedField(read_only=True)
    region = serializers.SlugRelatedField(slug_field='title', read_only=True)
    place = serializers.SlugRelatedField(slug_field='city', read_only=True)

    class Meta:
        model = Advert
        fields = ('title', 'category', 'price', 'is_new', 'region', 'place', 'main_photo')


class AdvertDetailSerializer(serializers.ModelSerializer):
    # Подробная информация об объявлении
    category = serializers.StringRelatedField(read_only=True)
    region = serializers.SlugRelatedField(slug_field='title', read_only=True)
    place = serializers.SlugRelatedField(slug_field='city', read_only=True)
    charvalues = ValueSerializer(many=True)
    gallery = GallerySerializer()
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    class Meta:
        model = Advert
        exclude = ('moderation', 'slug')


class AdvertCreateUpdateSerializer(serializers.ModelSerializer):
    # Добавление объявления
    gallery = serializers.StringRelatedField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Advert
        exclude = ('date', 'moderation', 'slug')

    #def create(self, request):
    #    request['user'] = self.context['request'].user    #
    #     advert = Advert.objects.create(**request)
    #     return advert

    def create(self, validated_data):
        gallery = self.initial_data.get('gallery')
        instance = super().create(validated_data)
        if gallery:
            serializer = GallerySerializer(data=gallery)
            serializer.is_valid(raise_exception=True)
            serializer.save(advert=instance)
        return instance