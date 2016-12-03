from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^enter$', views.enter, name='enter'),
    url(r'^delete/(?P<log_id>[0-9]+)$', views.delete, name='delete'),
    url(r'^$', views.list, name='list'),
]
