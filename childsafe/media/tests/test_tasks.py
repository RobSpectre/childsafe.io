from django.test import TestCase
from django.test import override_settings

import responses

from media.models import MediaItem
import media.tasks


@override_settings(TELLFINDER_API_KEY="xxxx",
                   PHOTODNA_API_KEY="yyyy")
class TestMediaTasks(TestCase):
    def setUp(self):
        self.mediaitem = MediaItem.objects.create(url="https://example.com/"
                                                  "stuff.png",
                                                  resource_id="derp")

    @responses.activate
    def test_scan_mediaitem_on_tellfinder(self):
        responses.add(responses.GET,
                      "https://example.com/stuff.png",
                      content_type="image/png",
                      body=open('media/tests/assets/example.png', 'rb'),
                      status=200)

        responses.add(responses.POST,
                      "https://api.tellfinder.com/similarimages",
                      json={"total": 5},
                      status=200)

        test = media.tasks.scan_mediaitem_on_tellfinder(self.mediaitem.id)

        self.assertTrue(test)
