from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=128, verbose_name='Название')
    description_short = models.TextField(
        blank=True, null=True, verbose_name='Краткое описание',
    )
    description_long = models.TextField(
        blank=True, null=True, verbose_name='Полное описание',
    )
    lng = models.FloatField(verbose_name='Долгота')
    lat = models.FloatField(verbose_name='Широта')

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, related_name='img_place',
        on_delete=models.CASCADE, verbose_name='Локация',
    )
    file = models.ImageField(verbose_name='Файл')
    position = models.PositiveIntegerField(
        default=0, blank=False, null=False, verbose_name='Позиция',
    )

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['position']

    def __str__(self):
        return f'{self.place.title} ({self.file})'
