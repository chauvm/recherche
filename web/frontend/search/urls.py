from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /search/
    url(r'^$', views.index, name='index'),    
]