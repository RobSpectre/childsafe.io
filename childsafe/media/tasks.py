import hashlib

from celery import shared_task

from django.conf import settings

from io import BytesIO

import requests

from .models import MediaItem


@shared_task
def scan_mediaitem(id):
    scan_mediaitem_on_tellfinder.apply_async(args=[id])

    return id


@shared_task
def scan_mediaitem_on_photodna(id):
    mediaitem = MediaItem.objects.get(id=id)

    uri = "https://api.microsoftmoderator.com/photodna/v1.0/Match"

    headers = {"Ocp-Apim-Subscription-Key": settings.PHOTODNA_API_KEY}

    payload = {"DataRepresentation": "URL",
               "Value": mediaitem.url}

    response = requests.post(uri,
                             headers=headers,
                             json=payload)

    if response.status_code == 200:
        response_json = response.json()

        if response_json['Status'].get('Code', None) == 3000:
            mediaitem.status = 'completed'
            mediaitem.scanned = True
            mediaitem.positive = response_json['IsMatch']
            mediaitem.save()
    else:
        return response.status_code


@shared_task
def scan_mediaitem_on_tellfinder(id):
    mediaitem = MediaItem.objects.get(id=id)

    image_response = requests.get(mediaitem.url)

    image_bytes = BytesIO(image_response.content)

    image_sha = hashlib.sha1()
    image_sha.update(image_bytes.getvalue())

    uri = "https://api.tellfinder.com/image/" \
          "{0}".format(image_sha.hexdigest())
    headers = {"x-api-key": settings.TELLFINDER_API_KEY}

    results = requests.get(uri, headers=headers)

    if results.status_code == 200:
        result_dict = results.json()

        if result_dict.get('total', None):
            mediaitem.positive = True

        mediaitem.scanned = True
        mediaitem.save()
    elif results.status_code == 404:
        mediaitem.scanned = True
        mediaitem.save()
    else:
        return results.status_code

    return results.json()
