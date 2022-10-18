import os
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone


def get_path_upload_image(file, username):
    # Создание пути для сохранения аватара пользователя
    time = timezone.now().strftime("%Y-%m-%d")
    end_extention = file.split('.')[1]
    head = file.split('.')[0]
    if len(head) > 10:
        head = head[:10]
    file_name = username + head + '.' + end_extention
    return os.path.join('{}', '{}').format(time, file_name)


class Profile(models.Model):
    # Профиль пользователя
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="profile")
    name = models.CharField("Имя", max_length=100)
    avatar = models.ImageField("Аватар", upload_to="profile/", blank=True, null=True)
    phone = models.CharField("Телефон", max_length=30)
    date = models.DateTimeField("Дата регистрации", auto_now_add=True)
    slug = models.SlugField("URL", max_length=50, default='')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = "{}-{}".format(self.user.id, self.user.username)
        self.avatar.name = get_path_upload_image(self.avatar.name, self.user.username)
        super().save(*args, **kwargs)

    #def get_absolute_url(self):
    #    return reverse("profile-detail", kwargs={"slug": self.user.username})

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # Создание профиля пользователя при регистрации
    if created:
        Profile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()