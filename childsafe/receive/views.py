from django.conf.urls import url, include
from django.contrib.auth.models import User

from rest_framework.decorators import detail_route
from rest_framework import routers, serializers, viewsets

from media.models import MediaItem


class MediaItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MediaItem
        fields = ('id', 'url', 'status', 'scanned', 'positive', 'alerted')


class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer


router = routers.DefaultRouter()
router.register(r'media', MediaItemViewSet)
