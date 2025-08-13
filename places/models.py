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

    def __str__(self):
        return self.title if len(self.title) <= 30 else self.title[:27] + '...'
