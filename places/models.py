from django.db import models


class Place(models.Model):

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    title = models.CharField(max_length=128, verbose_name='Название')
    placeId = models.SlugField(max_length=63, unique=True, verbose_name='Slug')
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    def __str__(self):
        return self.title


class Image(models.Model):

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, verbose_name='Локация'
    )
    file = models.ImageField(verbose_name='Файл')

    def __str__(self):
        return f'{self.place.title} ({self.file})'
