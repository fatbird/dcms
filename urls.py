from django.conf.urls import patterns, include, url

from .views import Dashboard

app_name = 'dcms'

urlpatterns = [
    url(r'^$', Dashboard.as_view(), name='dashboard')
]
