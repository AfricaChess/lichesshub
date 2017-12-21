from django.conf.urls import url

from tournament import views


urlpatterns = [
    #url('list/$', views.tournament_list, name='tournament_list'),
    url('register/(?P<id>\d+)/$', views.register, name='tournament_register'),
    url(
        'join/(?P<tournament_id>\d+)/(?P<player_id>\d+)/$',
        views.join,
        name='tournament_join'),
    url('pairings/(?P<id>\d+)/$', views.pairings, name='tournament_pairings'),
    url('pair/(?P<id>\d+)/$', views.run_pairings, name='run_pairings'),
    url('leaderboard/(?P<id>\d+)/$', views.leaderboard, name='leaderboard'),
]
