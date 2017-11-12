from celery import shared_task

from django.conf import settings

import requests

from clarifai.rest import ClarifaiApp
from twilio.rest import Client

from .models import MediaItem


@shared_task
def scan_mediaitem(id):
    scan_mediaitem_on_tellfinder.apply_async(args=[id])
    scan_mediaitem_on_clarifai_nsfw.apply_async(args=[id])
    scan_mediaitem_on_clarifai_moderation.apply_async(args=[id])

    mediaitem = MediaItem.objects.get(id=id)
    mediaitem.status = "scanning"
    mediaitem.save()

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

    uri = "https://api.tellfinder.com/similarimages"
    headers = {"x-api-key": settings.TELLFINDER_API_KEY}

    results = requests.post(uri, headers=headers,
                            json={"url": mediaitem.url})

    if results.status_code == 200:
        results_json = results.json()

        if results_json.get("similarUrls", None):
            mediaitem.positive = True

        mediaitem.scanned = True
        mediaitem.save()
    elif results.status_code == 404:
        mediaitem.scanned = True
        mediaitem.save()
    else:
        return results.status_code

    return results.json()


@shared_task
def scan_mediaitem_on_clarifai_nsfw(id):
    mediaitem = MediaItem.objects.get(id=id)
    clarifai_app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)

    model = clarifai_app.models.get('nsfw-v1.0')

    result = model.predict_by_url(url=mediaitem.url)

    if result['status']['code'] == 10000:
        for output in result['outputs']:
            if output.get('data', None):
                for concept in output['data']['concepts']:
                    if concept['name'] == 'nsfw' and concept['value'] >= 0.60:
                        mediaitem.positive = True
    else:
        return {"error": "Clarifai Failure", "result": result}

    mediaitem.scanned = True
    mediaitem.save()

    return result


@shared_task
def scan_mediaitem_on_clarifai_moderation(id):
    mediaitem = MediaItem.objects.get(id=id)
    clarifai_app = ClarifaiApp(api_key=settings.CLARIFAI_API_KEY)

    model = clarifai_app.models.get('moderation')

    result = model.predict_by_url(url=mediaitem.url)

    if result['status']['code'] == 10000:
        for output in result['outputs']:
            if output.get('data', None):
                for concept in output['data']['concepts']:
                    if concept['name'] == 'safe':
                        continue

                if concept['value'] >= 0.60:
                    mediaitem.positive = True
    else:
        return {"error": "Clarifai Failure", "result": result}

    mediaitem.scanned = True
    mediaitem.save()

    return result


@shared_task
def send_sms_notification(report):
    client = Client(settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN)

    mediaitem = MediaItem.objects.get(id=report['mediaitem_id'])

    body = "[Alert from childsafe.io]\n" \
           "Match Type: {0}\n" \
           "Resource ID: {1}\n" \
           "URI: {2}" \
           "".format(report['match_type'],
                     report['resource_id'],
                     report['url'])

    message = client.messages.create(from_=settings.TWILIO_PHONE_NUMBER,
                                     to=mediaitem.user.phone_number,
                                     body=body)

    return body
