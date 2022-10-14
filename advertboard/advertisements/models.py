import os
from django.contrib.auth.models import User
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from datetime import datetime
from django.utils import timezone
from . transliteration import transliteration


class Characteristic(models.Model):
    # Характеристики в рамках категорий
    full_name = models.CharField("Полное наименование", max_length=100, unique=True)
    name = models.CharField("Наименование", max_length=50)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"


class Value(models.Model):
    # Допустимые значения характеристик
    val = models.CharField("Значение", max_length=50, unique=True)
    characteristic = models.ForeignKey(Characteristic, verbose_name="Характеристика", related_name='values', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.characteristic.name, self.val)

    class Meta:
        verbose_name = "Значение"
        verbose_name_plural = "Значения характеристик"
        ordering = ('characteristic', 'id')


class Category(MPTTModel):
    # Категории объявлений
    full_name = models.CharField("Полное название", max_length=100, unique=True)
    name = models.CharField("Название", max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name="Родитель")
    characteristics = models.ManyToManyField(Characteristic, verbose_name="Характеристики", related_name='categories',
                                             blank=True)
    slug = models.SlugField("url", max_length=100, unique=True)

    def __str__(self):
        if self.parent:
            return '{} > {}'.format(self.parent, self.name)
        else:
            return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Region(models.Model):
    # Области и г. Минск
    title = models.CharField("Название", max_length=50, unique=True)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Область"
        verbose_name_plural = "Области/г.Минск"
        ordering = ('id',)


class Place(models.Model):
    # Местоположение (города или районы г. Минска)
    city = models.CharField("Город/район", max_length=50, unique=True)
    region = models.ForeignKey(Region, verbose_name="Область", on_delete=models.CASCADE)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return '{}, {}'.format(self.region, self.city)

    class Meta:
        verbose_name = "Город/район"
        verbose_name_plural = "Города/районы"
        ordering = ('region', 'city')


class Advert(models.Model):
    # Объявления
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    title = models.CharField("Заголовок", max_length=200)
    category = TreeForeignKey(Category, verbose_name="Категория", related_name='adverts', on_delete=models.CASCADE)
    charvalues = ChainedManyToManyField(Value, chained_field="category",
                                        chained_model_field="characteristic__categories", auto_choose=True,
                                        horizontal=True, verbose_name="Значения характеристик")
    description = models.TextField("Описание", max_length=5000)
    is_new = models.CharField("Состояние", max_length=5, choices=[('1', 'Новое'), ('2', 'Б/у')])
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2, blank=True, null=True)
    region = models.ForeignKey(Region, verbose_name="Регион", related_name='adverts', on_delete=models.CASCADE)
    place = ChainedForeignKey(Place, chained_field="region", chained_model_field="region", show_all=True,
                              auto_choose=True, sort=True, verbose_name="Местоположение", related_name='adverts',
                              on_delete=models.CASCADE)
    phone_1 = models.CharField("Телефон", max_length=30, blank=True, null=True)
    phone_2 = models.CharField("Телефон", max_length=30, blank=True, null=True)
    date = models.DateTimeField("Дата создания или обновления", auto_now=True)
    moderation = models.BooleanField("Модерация", default=False)
    slug = models.SlugField("url", max_length=200, unique=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.title)

    def get_absolute_url(self):
        return reverse("advert-detail", kwargs={"category": self.category.slug, "slug": self.slug})

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Gallery(models.Model):
    # Галерея фото
    advert = models.OneToOneField(Advert, verbose_name="Объявление", related_name='gallery', on_delete=models.CASCADE)
    date = models.DateTimeField("Дата создания или обновления", auto_now=True)
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return str(self.advert)

    class Meta:
        verbose_name = "Галерея"
        verbose_name_plural = "Галереи"

@receiver(post_save, sender=Advert)
def create_advert_gallery(sender, instance, created, **kwargs):
    # Создание галереи при создании объявления
    if created:
        Advert.objects.filter(id=instance.id).update(slug=str(instance.id) + '-' + transliteration(instance.title))
        Gallery.objects.create(advert=instance, slug='gallery-{}-{}'.format(transliteration(instance.title), instance.id))

@receiver
def save_advert_gallery(sender, instance, **kwargs):
    instance.gallery.save()


def get_path_upload_image(file, gallery):
    # Создание пути для сохранения фото
    time = timezone.now().strftime("%Y-%m-%d")
    end_extention = file.split('.')[1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = head + '.' + end_extention
    return os.path.join('{}', '{}', '{}').format(time, gallery, file_name)


class Photo(models.Model):
    # Фотографии
    name = models.CharField("Имя", max_length=50, null=True, blank=True)
    gallery = models.ForeignKey(Gallery, verbose_name="Галерея", related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField("Фото", upload_to="advertisements/")
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return '{}'.format(self.image.name)[15:]


    def save(self, *args, **kwargs):
        trans_gallery = transliteration(self.gallery)
        self.slug = '{}-{}'.format(trans_gallery, self.image.name)
        self.image.name = get_path_upload_image(self.image.name, trans_gallery)
        super().save(*args, **kwargs)

        # if self.image:
        #     img = Image.open(self.image.path)
        #     if img.height > 200 or img.width > 200:
        #         output_size = (200, 200)
        #         img.thumbnail(output_size)
        #         img.save(self.image.path)

    class Meta:
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"





