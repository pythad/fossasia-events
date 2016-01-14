from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.EventListView.as_view(), name='events'),
    url(r'^statistics/$', views.EventsStatistics.as_view(), name='events_stats'),
    url(r'^participate/$', views.participate, name='participate'),
    url(r'^get_attendees/$', views.get_attendees, name='get_attendees'),
    url(r'^(?P<pk>\d+)/$', views.EventDetailView.as_view(), name='event'),
    url(r'^(?P<pk>\d+)/edit/$', views.EventUpdateView.as_view(), name='event_edit'),
    url(r'^add/$', views.EventCreateView.as_view(), name='event_create'),
    url(r'^send_notification/$', views.SendNotification.as_view(), name='send_notification'),
]
