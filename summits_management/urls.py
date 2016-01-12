from django.conf.urls import url, include
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^$', views.Home.as_view(), name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^accounts/profile/(?P<pk>\d+)/(?P<username>[a-z0-9_-]+)/$', views.UserDetailView.as_view(), name='account_profile'),
    url(r'^accounts/profile/(?P<pk>\d+)/(?P<username>[a-z0-9_-]+)/edit/$', views.UserUpdateView.as_view(), name='account_profile_edit'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^inbox/notifications/', include('notifications.urls', namespace='notifications')),
]
