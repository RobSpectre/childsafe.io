from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login_view, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^user/profile/', views.profile, name='profile'),
    url(r'^documentation/', views.documentation, name='documentation')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
