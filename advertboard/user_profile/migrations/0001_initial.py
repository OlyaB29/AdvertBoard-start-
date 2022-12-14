# Generated by Django 4.1.1 on 2022-10-06 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Аватар')),
                ('phone', models.CharField(max_length=30, verbose_name='Телефон')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('slug', models.SlugField(default='', verbose_name='URL')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
