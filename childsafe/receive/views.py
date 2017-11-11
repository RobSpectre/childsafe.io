from rest_framework import routers, serializers, viewsets

from media.models import MediaItem
from web.models import ChildsafeUser


class ChildsafeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildsafeUser

        fields = ['id']


class MediaItemSerializer(serializers.ModelSerializer):
    user = ChildsafeUserSerializer(read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=ChildsafeUser.objects.all(),
        source='user',
        write_only=True)

    class Meta:
        model = MediaItem

        fields = ('id',
                  'resource_id',
                  'url',
                  'status',
                  'scanned',
                  'positive',
                  'alerted',
                  'user',
                  'user_id')


class MediaItemViewSet(viewsets.ModelViewSet):
    queryset = MediaItem.objects.all()
    serializer_class = MediaItemSerializer


router = routers.DefaultRouter()
router.register(r'media', MediaItemViewSet)
