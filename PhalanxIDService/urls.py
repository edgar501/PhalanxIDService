from django.conf.urls import include, url
from django.contrib import admin
from WebService.views import PhalanxIDView, PhalanxIDUpdateDeleteView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', PhalanxIDView.as_view(), name='phalanx_id'),
    url(r'^edit/(?P<pk>[0-9]+)$', PhalanxIDUpdateDeleteView.as_view(), name='phalanx_id_delete'),
]
