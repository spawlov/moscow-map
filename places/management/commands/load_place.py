import os
import shutil
import requests
from loguru import logger

from django.conf import settings
from django.core.management import BaseCommand

from places.models import Place, Image


class Command(BaseCommand):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/39.0.2171.95 Safari/537.36'
    }

    def handle(self, *args, **options):
        place_path = options.get('place', '')
        try:
            with requests.get(place_path, headers=self.headers) as resp:
                if resp.status_code == 200:
                    logger.info('Server response is "OK"')
                    resp_json = resp.json()
                    cords = resp_json.get('coordinates', None)
                    place, created = Place.objects.get_or_create(
                        title=resp_json.get('title', None),
                        description_short=resp_json.get(
                            'description_short', None
                        ),
                        description_long=resp_json.get(
                            'description_long', None
                        ),
                        lng=cords.get('lng', None),
                        lat=cords.get('lat', None)
                    )
                    if created:
                        # If locate created
                        # Create Dir if not exist
                        if not os.path.exists(settings.MEDIA_ROOT):
                            os.makedirs(settings.MEDIA_ROOT)
                        # Saving files
                        for image in resp_json.get('imgs'):
                            file = requests.get(image, stream=True)
                            file_path = f"media/{str(image).split('/')[-1]}"
                            with open(file_path, 'wb') as f:
                                file.raw.decode_content = True
                                shutil.copyfileobj(file.raw, f)
                            img_qs, img_cr = Image.objects.get_or_create(
                                place_id=place.id,
                                file=str(image).split('/')[-1]
                            )
                            if not img_cr:
                                logger.warning('This record(s) already exists')
                            logger.info(
                                f'The record is created, '
                                f'the file {image} is saved'
                            )
                    else:
                        logger.warning('This record(s) already exists')
        except Exception as e:
            logger.error(f'Error: {e}')
        else:
            logger.info('Success...')


    def add_arguments(self, parser):
        parser.add_argument('place', action='store')
