from .. import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^donation-trigger/$', views.donation_trigger, name='onepercent-afom-donation-trigger'),
)
