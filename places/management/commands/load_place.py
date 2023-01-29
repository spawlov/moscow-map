import os
import shutil

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import BaseCommand
from loguru import logger

from places.models import Place, Image


class Command(BaseCommand):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }

    def __init__(self):
        super().__init__()
        self.place_raw = {}

    @property
    def add_or_update_place(self) -> tuple:
        """
        Adding a location if there are no such coordinates
        or updating an existing one
        """
        try:
            title: str = self.place_raw['title']
            lng: float = self.place_raw['coordinates']['lng']
            lat: float = self.place_raw['coordinates']['lat']
        except KeyError as e:
            logger.error(f'Key {e} invalid')
            return None, False

        description_short = self.place_raw.get('description_short', '')
        description_long = self.place_raw.get('description_long', '')

        place, created = Place.objects.update_or_create(
            lng=lng,
            lat=lat,
            defaults={
                'title': title,
                'description_short': description_short,
                'description_long': description_long,
            },
        )
        if created:
            logger.info(f'Location "{title}" saved')
        else:
            logger.info(f'Location "{title}" updated')
        return place, created

    def saving_images(self, place_id: int) -> None:
        """Saving images for location"""
        try:
            images: list = self.place_raw['imgs']
        except KeyError as e:
            logger.error(f'Key {e} invalid')
            return

        for image in images:
            if not os.path.exists(
                    os.path.join(settings.MEDIA_ROOT, str(place_id))
            ):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, str(place_id)))

            image_name = image.split('/')[-1]
            full_image_name = os.path.join(str(place_id), image_name)

            image_content = ContentFile(
                requests.get(image, stream=True).content, name=full_image_name
            )
            image = Image()
            image.place_id = place_id
            image.file = image_content
            image.save()

            logger.info(f'The file: "{full_image_name}" saved')

    def handle(self, *args, **options):
        try:
            with requests.get(
                    options['place'], headers=self.headers
            ) as response:
                if not response.ok:
                    logger.error(
                        f'''Server response is: 
                        {response.url}::->::{response.status_code}'''
                    )
        except Exception as e:
            logger.error(e)
        else:
            self.place_raw = response.json()
            logger.info('Server response is "OK"')
            place, place_created = self.add_or_update_place
            if place_created:
                self.saving_images(place.id)

    def add_arguments(self, parser):
        parser.add_argument('place', action='store')
