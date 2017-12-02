from django.conf.urls import url

from tournament import views


urlpatterns = [
    url('list/$', views.tournament_list, name='tournament_list'),
    url('register/(?P<id>\d+)/$', views.register, name='tournament_register'),
    url(
        'join/(?P<tournament_id>\d+)/(?P<player_id>\d+)/$',
        views.join,
        name='tournament_join'),
]
