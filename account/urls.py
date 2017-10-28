from django.conf.urls import url

from account import views


urlpatterns = [
    url(r'profile/$', views.profile),
    url(r'pay/$', views.pay),
    url(r'save_game/$', views.save_game),
    url(r'get_result/(?P<id>\d+)/$', views.get_result),
]
