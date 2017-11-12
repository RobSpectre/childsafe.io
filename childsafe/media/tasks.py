from celery import shared_task

from django.conf import settings

import requests

from clarifai.rest import ClarifaiApp
from twilio.rest import Client

from .models import MediaItem
from .models import Match


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
            if response_json['IsMatch']:
                match = Match(resource_id=mediaitem.resource_id,
                              url=mediaitem.url,
                              risk="Child Pornography",
                              user=mediaitem.user,
                              mediaitem=mediaitem)
                match.save()
    else:
        return response.status_code

    return response_json


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
            match = Match(resource_id=mediaitem.resource_id,
                          url=mediaitem.url,
                          risk="Human Trafficking",
                          user=mediaitem.user,
                          mediaitem=mediaitem)
            match.save()

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
                    if concept['name'] == 'nsfw' and concept['value'] >= 0.70:
                        match = Match(resource_id=mediaitem.resource_id,
                                      url=mediaitem.url,
                                      risk="NSFW",
                                      user=mediaitem.user,
                                      mediaitem=mediaitem)
                        match.save()
    else:
        return {"error": "Clarifai Failure", "result": result}

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

                    if concept['value'] >= 0.70:
                        match = Match(resource_id=mediaitem.resource_id,
                                      url=mediaitem.url,
                                      risk="Graphic Content",
                                      user=mediaitem.user,
                                      mediaitem=mediaitem)
                        match.save()
    else:
        return {"error": "Clarifai Failure", "result": result}

    return result


@shared_task
def notify_match(id):
    match = Match.objects.get(id=id)

    client = Client(settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN)

    body = "[Alert from childsafe.io]\n" \
           "Risk: {0}\n" \
           "Resource ID: {1}\n" \
           "URI: {2}" \
           "".format(match.risk,
                     match.resource_id,
                     match.url)

    client.messages.create(from_=settings.TWILIO_PHONE_NUMBER,
                           to=match.user.phone_number,
                           body=body)

    return body
