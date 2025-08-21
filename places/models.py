import textwrap

from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        max_length=70,
        verbose_name='Название места или мероприятия'
    )
    short_description = models.TextField(
        verbose_name='Краткое описание',
        blank=True
    )
    long_description  = HTMLField(
        verbose_name='Подробное описание',
        blank=True
    )
    lat = models.FloatField(verbose_name='Широта')
    lng = models.FloatField(verbose_name='Долгота')

    class Meta:
        verbose_name = 'Место'
        verbose_name_plural = 'Места'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'lat', 'lng'],
                name='unique_place_title_lat_lng'
            )
        ]

    def __str__(self):
        return textwrap.shorten(self.title, 30, placeholder="...")


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место или событие, к которому относится изображение'
    )
    image = models.ImageField(
        upload_to='places/',
        verbose_name='Директория для сохранения изображений'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Порядковый номер картинки в галерее'
    )

    def image_preview(self):
        try:
            return format_html(
                '<img src="{}" style="object-fit: contain; max-width: 150px" />',
                self.image.url
            )
        except (ValueError, AttributeError):
            return '-'

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображения места'
        verbose_name_plural = 'Изображения мест'
        indexes = [
            models.Index(fields=['place', 'order']),
        ]

    def __str__(self):
        return f'{self.id} — {self.place.title}'