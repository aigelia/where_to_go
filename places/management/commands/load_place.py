import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from places.models import Place, PlaceImage


class Command(BaseCommand):
    help = 'Автоматическая загрузка новых мест из json-файлов в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            'json_url',
            type=str,
            help='URL для загрузки JSON с данными'
        )

    def handle(self, *args, **options):
        json_url = options['json_url']
        self.stdout.write(f'Загружаем данные с {json_url}...')

        response = requests.get(json_url)
        response.raise_for_status()

        try:
            data = response.json()
        except ValueError:
            self.stderr.write('Ошибка: полученные данные не являются JSON')
            return

        lat = data.get('coordinates', {}).get('lat')
        lng = data.get('coordinates', {}).get('lng')

        place, created = Place.objects.get_or_create(
            title=data.get('title'),
            defaults={
                'short_description': data.get('description_short'),
                'long_description': data.get('description_long'),
                'lat': lat,
                'lng': lng,
            }
        )
        if created:
            self.stdout.write('Объект создан. Загружаем картинки...')
        else:
            self.stdout.write('Объект уже существовал. Загрузка остановлена.')
            return

        for url in data.get('imgs', []):
            image_name = url.split('/')[-1]

            if PlaceImage.objects.filter(place=place, image=f'places/{image_name}').exists():
                self.stdout.write(f'Изображение {image_name} уже существует, пропускаем...')
                continue

            try:
                img_response = requests.get(url)
                img_response.raise_for_status()
            except requests.RequestException as e:
                self.stderr.write(f'Не удалось загрузить {url}: {e}')
                continue

            place_image = PlaceImage(place=place)
            place_image.image.save(image_name, ContentFile(img_response.content), save=True)
            self.stdout.write(f'Добавлено изображение {image_name}')

        self.stdout.write('Загрузка завершена')
        return