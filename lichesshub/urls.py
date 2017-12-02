"""lichesshub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from django.views.generic.base import TemplateView
from core.views import forgot, change_pwd, register
from club.views import profile, grandprix
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/forgot/$', forgot, name='forgot_password'),
    url(r'^accounts/register/$', register, name='register'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^$', profile, name='home'),
    url(r'^grandprix/$', grandprix, name='grandprix'),
    url(r'^accounts/sent/$', TemplateView.as_view(template_name='core/email_sent.html'), name='email_sent'),
    url(r'^accounts/notsent/$', TemplateView.as_view(template_name='core/not_sent.html'), name='not_sent'),
    url(r'^accounts/pwdset/$', TemplateView.as_view(template_name='core/pwd_set.html'), name='pwd_set'),
    url(r'^accounts/change_pwd/(?P<id>\d+)/$', change_pwd, name='change_pwd'),
    url(r'^account/', include('account.urls')),
    url(r'^tournament/', include('tournament.urls')),
    url(r'^club/', include('club.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = 'Africa Lichess Hub'
