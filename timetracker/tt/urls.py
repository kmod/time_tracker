from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^enter$', views.enter, name='enter'),
    url(r'^$', views.list, name='list'),
]
