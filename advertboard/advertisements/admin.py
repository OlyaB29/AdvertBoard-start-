from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from . models import Category, Characteristic, Value, Advert, Place, Region, Gallery, Photo


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    #  Категории
    list_display = ('name', 'parent', 'id')
    prepopulated_fields = {'slug': ('full_name',)}
    mptt_level_indent = 20
    search_fields = ("name", "parent")


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    #  Характеристики
    list_display = ('id', 'name', 'full_name')
    list_display_links = ('name',)
    list_filter = ('categories',)
    prepopulated_fields = {'slug': ('full_name',)}
    search_fields = ("name", )


@admin.register(Value)
class ValueAdmin(admin.ModelAdmin):
    #  Значения характеристик
    list_display = ('id', 'characteristic', 'val')
    list_filter = ('characteristic',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    #  Местоположение
    list_display = ('id', 'city', 'region')
    list_display_links = ('city',)
    list_filter = ('region',)
    prepopulated_fields = {'slug': ('city',)}


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    # Области и г. Минск
    list_display = ('id', 'title')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    #  Объявления
    list_display = ('id', 'title', 'user', 'category', 'is_new', 'price', 'region', 'place', 'date', 'moderation')
    list_filter = ('user', 'category', 'is_new', 'region', 'place', 'date', 'moderation', 'price')
    list_editable = ('moderation',)
    search_fields = ('user', 'title', 'category__name', 'region', 'place')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    # Галерея фото
    list_display = ('id', 'advert', 'date')
    list_display_links = ('advert',)
    list_filter = ('date',)
   # prepopulated_fields = {'slug': ('advert',)}


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    # Фотографии
    list_display = ('id', 'name', 'gallery', 'image')
    list_filter = ('gallery',)
    prepopulated_fields = {'slug': ('name',)}