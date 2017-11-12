from mock import patch

from django.test import TestCase
from django.test import override_settings

import responses

from media.models import MediaItem
from media.models import Match
import media.tasks


@override_settings(TELLFINDER_API_KEY="xxxx",
                   PHOTODNA_API_KEY="yyyy")
class TestMediaTasks(TestCase):
    @patch('media.tasks.scan_mediaitem.apply_async')
    def setUp(self, mock_scan):
        self.mediaitem = MediaItem.objects.create(url="https://example.com/"
                                                  "stuff.png",
                                                  resource_id="derp")

    @responses.activate
    @patch('media.tasks.notify_match.apply_async')
    def test_scan_mediaitem_on_tellfinder(self, mock_notify):
        responses.add(responses.GET,
                      "https://example.com/stuff.png",
                      content_type="image/png",
                      body=open('media/tests/assets/example.png', 'rb'),
                      status=200)

        responses.add(responses.POST,
                      "https://api.tellfinder.com/similarimages",
                      json={"similarUrls": ["https://backderp.com/derp.jpg"]},
                      status=200)

        media.tasks.scan_mediaitem_on_tellfinder(self.mediaitem.id)

        test_item = MediaItem.objects.get(id=self.mediaitem.id)

        matches = Match.objects.all()

        self.assertEquals(len(matches), 1)
        self.assertTrue(mock_notify.called)
