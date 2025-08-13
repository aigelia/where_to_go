from django.db import models


class Place(models.Model):
    title = models.CharField(
        max_length=70,
        verbose_name='Название места или мероприятия'
    )
    description_short = models.TextField(
        max_length=300,
        verbose_name='Краткое описание (до 300 символов)'
    )
    description_long  = models.TextField(verbose_name='Подробное описание')
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
    description = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Изображения места"
        verbose_name_plural = "Изображения мест"

    def __str__(self):
        return f"{self.id} — {self.place.title}"