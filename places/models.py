from django.db import models
from django.utils.html import format_html
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        max_length=70,
        verbose_name='Название места или мероприятия'
    )
    description_short = models.CharField(
        verbose_name='Краткое описание (до 255 символов)',
        blank=True
    )
    description_long  = HTMLField(
        verbose_name='Подробное описание',
        blank=True
    )
    lat = models.FloatField(verbose_name='Широта')
    lng = models.FloatField(verbose_name='Долгота')

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title if len(self.title) <= 30 else self.title[:27] + '...'


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='places/')
    order = models.PositiveIntegerField(default=0)

    def image_preview(self):
        try:
            return format_html(
                '<img src="{}" width="150" style="object-fit: contain;" />',
                self.image.url
            )
        except (ValueError, AttributeError):
            return "-"

    class Meta:
        ordering = ['order']
        verbose_name = "Изображения места"
        verbose_name_plural = "Изображения мест"

    def __str__(self):
        return f"{self.id} — {self.place.title}"