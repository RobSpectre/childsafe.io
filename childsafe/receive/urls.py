from django.conf.urls import url
from django.conf.urls import include

from .views import router


urlpatterns = [
    url(r'^', include(router.urls)),
]
