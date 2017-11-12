from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login_page, name='login'),
    url(r'^user/profile/', views.profile, name='profile'),
    url(r'^docs/$', views.docs_index, name='docs_index'),
    url(r'^docs/aws-s3$', views.docs_aws, name='docs_aws'),
    url(r'^docs/google-cloud-storage$', views.docs_gcs, name='docs_gcs'),
    url(r'^docs/azure$', views.docs_azure, name='docs_azure'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
