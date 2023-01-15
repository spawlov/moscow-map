import shutil

import requests

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
                        for image in resp_json.get('imgs'):
                            file = requests.get(image, stream=True)
                            file_path = f"media/{str(image).split('/')[-1]}"
                            with open(file_path, 'wb') as f:
                                file.raw.decode_content = True
                                shutil.copyfileobj(file.raw, f)
                            Image.objects.get_or_create(
                                place_id=place.id,
                                file=str(image).split('/')[-1]
                            )

        except Exception as e:
            print(f'Error: {e}')

    def add_arguments(self, parser):
        parser.add_argument('place', action='store')
