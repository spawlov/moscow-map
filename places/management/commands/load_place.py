import os
import shutil

import requests
from django.conf import settings
from django.core.management import BaseCommand
from loguru import logger

from places.models import Place, Image


class Command(BaseCommand):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }

    def add_or_update_place(self, place_path: str) -> tuple:
        """
        Adding a location if there are no such coordinates
        or updating an existing one
        """
        try:
            with requests.get(place_path, headers=self.headers) as resp:
                if not resp.ok:
                    logger.error(
                        f'''Server response is: 
                        {resp.url}::->::{resp.status_code}'''
                    )
                    return None, False, None
            resp_json = resp.json()
            logger.info('Server response is "OK"')
            cords = resp_json.get('coordinates', None)
            # Validate Coordinates
            if not cords:
                logger.error('Coordinates is empty')
                return None, False, resp_json
            elif any([not cords.get('lng', None), not cords.get('lat', None)]):
                logger.error(f'Invalid coordinates')
                return None, False, resp_json
            # Validate Title
            title = resp_json.get('title', None)
            if not title:
                logger.error('Title is empty')
                return None, False, resp_json

            description_short = resp_json.get('description_short', None)
            description_long = resp_json.get('description_long', None)

            place, created = Place.objects.update_or_create(
                lng=cords['lng'],
                lat=cords['lat'],
                defaults={
                    'title': title,
                    'description_short': description_short,
                    'description_long': description_long,
                },
            )
            return place, created, resp_json
        except Exception as e:
            logger.error(e)
            return None, False, None

    @staticmethod
    def saving_images(place, resp_json):
        """ We save the creations for the location """
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        # Saving files
        for image in resp_json.get('imgs'):
            file = requests.get(image, stream=True)
            file_path = f'{settings.MEDIA_ROOT}/{str(image).split("/")[-1]}'
            with open(file_path, 'wb') as f:
                file.raw.decode_content = True
                shutil.copyfileobj(file.raw, f)
                images_qs, images_created = Image.objects.get_or_create(
                    place_id=place.id,
                    file=str(image).split('/')[-1]
                )
                if not images_created:
                    logger.warning('This file(s) already exists')
                logger.info(
                    f'The file {str(image).split("/")[-1]} is saved'
                )

    def handle(self, *args, **options):
        place, place_created, resp_json = self.add_or_update_place(
            options['place']
        )
        if not place_created:
            logger.info(
                f'The location already exists, the record has been updated'
            )
        else:
            self.saving_images(place, resp_json)

    def add_arguments(self, parser):
        parser.add_argument('place', action='store')
