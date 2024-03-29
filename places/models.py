import os

from django.db import models

from django_ckeditor_5.fields import CKEditor5Field


def get_uploading_path(instance, filename):
    return os.path.join(str(instance.place.id), filename)


class Place(models.Model):
    title = models.CharField(max_length=128, verbose_name="Название")
    description_short = models.TextField(
        blank=True,
        verbose_name="Краткое описание",
    )
    description_long = CKEditor5Field(
        config_name="extends",
        blank=True,
        verbose_name="Полное описание",
    )
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Локация",
    )
    file = models.ImageField(upload_to=get_uploading_path, verbose_name="Файл")
    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиция",
    )

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ["position"]

    def __str__(self):
        return f"{self.place.title} ({self.file})"
