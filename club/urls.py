from django.conf.urls import url

from club import views


urlpatterns = [
    url(r'info/$', views.info, name='club_info'),
    url(r'add_member/$', views.add_member),
    url(r'remove_member/(?P<id>\d+)/$', views.remove_member),
    url(r'save_order/$', views.save_order),
    url(r'cancel_match/(?P<id>\d+)/$', views.cancel_match),
    url(r'start_match/(?P<id>\d+)/$', views.start_match),
    url(r'complete_match/(?P<id>\d+)/$', views.complete_match),
    url(r'leaderboard/$', views.leaderboard),
]
